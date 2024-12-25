#!/bin/bash

# Default values
DEFAULT_PORT="8000"
DEFAULT_ENV_TAG="Environment"
DEFAULT_ENV_VALUE="prod"
DEFAULT_NAME_TAG="Name"
DEFAULT_NAME_VALUE="emogi-ec2-app"
DEFAULT_HEALTH_PATH="health"
DEFAULT_CHECK_COUNT="10"
DEFAULT_CHECK_INTERVAL="2"
DEFAULT_SUCCESS_THRESHOLD="3"

# Help function
show_help() {
    echo "🔍 Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -p, --port <port>        Application port to check (default: $DEFAULT_PORT)"
    echo "  --env-tag <tag>          EC2 environment tag key (default: $DEFAULT_ENV_TAG)"
    echo "  --env-value <value>      EC2 environment tag value (default: $DEFAULT_ENV_VALUE)"
    echo "  --name-tag <tag>         EC2 name tag key (default: $DEFAULT_NAME_TAG)"
    echo "  --name-value <value>     EC2 name tag value (default: $DEFAULT_NAME_VALUE)"
    echo "  --path <path>            Health check endpoint path (default: $DEFAULT_HEALTH_PATH)"
    echo "  -c, --count <number>     Number of health checks to perform (default: $DEFAULT_CHECK_COUNT)"
    echo "  -i, --interval <seconds> Interval between checks in seconds (default: $DEFAULT_CHECK_INTERVAL)"
    echo "  -s, --success <number>   Number of successes needed to pass (default: $DEFAULT_SUCCESS_THRESHOLD)"
    echo "  -h, --help               Show this help message"
    echo
    echo "Examples:"
    echo "Basic Usage:"
    echo "  # Check health with default settings (10 attempts, needs 3 successes)"
    echo "  $0"
    echo
    echo "Custom Settings:"
    echo "  # 5 successes out of 15 attempts to pass"
    echo "  $0 -c 15 -s 5"
    echo
    echo "Quick Check:"
    echo "  # Fast check with 1 second interval"
    echo "  $0 -i 1"
    echo
    echo "Different Environment:"
    echo "  # Check staging environment"
    echo "  $0 --env-value staging --name-value emogi-ec2-staging"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        --env-tag)
            ENV_TAG="$2"
            shift 2
            ;;
        --env-value)
            ENV_VALUE="$2"
            shift 2
            ;;
        --name-tag)
            NAME_TAG="$2"
            shift 2
            ;;
        --name-value)
            NAME_VALUE="$2"
            shift 2
            ;;
        --path)
            HEALTH_PATH="$2"
            shift 2
            ;;
        -c|--count)
            CHECK_COUNT="$2"
            shift 2
            ;;
        -i|--interval)
            CHECK_INTERVAL="$2"
            shift 2
            ;;
        -s|--success)
            SUCCESS_THRESHOLD="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "❌ Unknown option: $1"
            show_help
            ;;
    esac
done

# Set default values if not provided
PORT=${PORT:-$DEFAULT_PORT}
ENV_TAG=${ENV_TAG:-$DEFAULT_ENV_TAG}
ENV_VALUE=${ENV_VALUE:-$DEFAULT_ENV_VALUE}
NAME_TAG=${NAME_TAG:-$DEFAULT_NAME_TAG}
NAME_VALUE=${NAME_VALUE:-$DEFAULT_NAME_VALUE}
HEALTH_PATH=${HEALTH_PATH:-$DEFAULT_HEALTH_PATH}
CHECK_COUNT=${CHECK_COUNT:-$DEFAULT_CHECK_COUNT}
CHECK_INTERVAL=${CHECK_INTERVAL:-$DEFAULT_CHECK_INTERVAL}
SUCCESS_THRESHOLD=${SUCCESS_THRESHOLD:-$DEFAULT_SUCCESS_THRESHOLD}

# Find EC2 instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:${ENV_TAG},Values=${ENV_VALUE}" "Name=tag:${NAME_TAG},Values=${NAME_VALUE}" \
    --query "Reservations[0].Instances[0].InstanceId" \
    --output text)

# Commands to execute
read -r -d '' COMMANDS << EOF
echo "🏥 Starting health check (need ${SUCCESS_THRESHOLD} successes out of ${CHECK_COUNT} attempts)..."

success_count=0
for ((i=1; i<=${CHECK_COUNT}; i++)); do
    http_code=\$(curl -s -w '%{http_code}' -o /dev/null --connect-timeout 5 --max-time 5 http://localhost:${PORT}/${HEALTH_PATH})
    
    if [ "\$http_code" -eq 200 ]; then
        ((success_count++))
        echo "✅ Check #\$i successful (HTTP \$http_code) - Success count: \$success_count"
        
        if [ \$success_count -ge ${SUCCESS_THRESHOLD} ]; then
            echo "🎉 Health check passed! (\$success_count successes achieved)"
            exit 0
        fi
    else
        echo "⚠️ Check #\$i failed (HTTP \$http_code) - Success count: \$success_count"
    fi
    
    remaining_needed=\$((${SUCCESS_THRESHOLD} - success_count))
    remaining_checks=\$((${CHECK_COUNT} - i))
    
    if [ \$remaining_needed -gt \$remaining_checks ]; then
        echo "❌ Health check failed: Cannot reach ${SUCCESS_THRESHOLD} successes in remaining attempts"
        echo "   Current success count: \$success_count"
        echo "   Remaining checks: \$remaining_checks"
        echo "   Still needed: \$remaining_needed"
        exit 1
    fi
    
    if [ \$i -lt $CHECK_COUNT ]; then
        sleep $CHECK_INTERVAL
    fi
done

if [ \$success_count -ge ${SUCCESS_THRESHOLD} ]; then
    echo "🎉 Health check passed! (\$success_count successes out of ${CHECK_COUNT} attempts)"
    exit 0
else
    echo "❌ Health check failed: Only achieved \$success_count successes out of ${CHECK_COUNT} attempts"
    exit 1
fi
EOF

if [ -n "$INSTANCE_ID" ]; then
    echo "🔍 Initiating health check process..."
    
    # Convert commands to JSON array
    COMMANDS_JSON=$(echo "$COMMANDS" | jq -R -s 'split("\n")[:-1]')
    
    # Execute command and store Command ID
    COMMAND_ID=$(aws ssm send-command \
        --instance-ids "$INSTANCE_ID" \
        --document-name "AWS-RunShellScript" \
        --parameters "{\"commands\": $COMMANDS_JSON}" \
        --output text \
        --query "Command.CommandId")
    
    echo "📤 Health check initiated! (Command ID: $COMMAND_ID)"
    
    # Monitor command execution status
    while true; do
        STATUS=$(aws ssm list-command-invocations \
            --command-id "$COMMAND_ID" \
            --details \
            --query "CommandInvocations[0].Status" \
            --output text)
        
        if [ "$STATUS" == "Success" ]; then
            echo "✅ Health check monitoring completed!"
            
            # Show execution results without pager
            aws ssm get-command-invocation \
                --command-id "$COMMAND_ID" \
                --instance-id "$INSTANCE_ID" \
                --query "StandardOutputContent" \
                --output text | cat
            break
        elif [ "$STATUS" == "Failed" ] || [ "$STATUS" == "Cancelled" ] || [ "$STATUS" == "TimedOut" ]; then
            echo "🚨 Health check monitoring failed! (Status: $STATUS)"
            echo "❌ Error details:"
            aws ssm get-command-invocation \
                --command-id "$COMMAND_ID" \
                --instance-id "$INSTANCE_ID" \
                --query "StandardErrorContent" \
                --output text | cat
            exit 1
        fi
        
        echo "⏳ Checking... (Status: $STATUS)"
        sleep 2
    done
else
    echo "❌ Target instance not found!"
fi