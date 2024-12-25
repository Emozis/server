#!/bin/bash

# Default values
DEFAULT_IMAGE_TAG="latest"
DEFAULT_CONTAINER_NAME="app"
DEFAULT_PORT="8000"
DEFAULT_ENV="prod"
DEFAULT_IMAGE_NAME="isakin/emogi-prod"
DEFAULT_ENV_TAG="Environment"
DEFAULT_ENV_VALUE="prod"
DEFAULT_NAME_TAG="Name"
DEFAULT_NAME_VALUE="emogi-ec2-app"

# Help function
show_help() {
    echo "🔍 Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -t, --tag <tag>          Docker image tag (default: $DEFAULT_IMAGE_TAG)"
    echo "  -n, --name <name>        Container name (default: $DEFAULT_CONTAINER_NAME)"
    echo "  -p, --port <port>        Container port (default: $DEFAULT_PORT)"
    echo "  -e, --env <env>          Environment (default: $DEFAULT_ENV)"
    echo "  -i, --image <image>      Docker image name (default: $DEFAULT_IMAGE_NAME)"
    echo "  --env-tag <tag>          EC2 environment tag key (default: $DEFAULT_ENV_TAG)"
    echo "  --env-value <value>      EC2 environment tag value (default: $DEFAULT_ENV_VALUE)"
    echo "  --name-tag <tag>         EC2 name tag key (default: $DEFAULT_NAME_TAG)"
    echo "  --name-value <value>     EC2 name tag value (default: $DEFAULT_NAME_VALUE)"
    echo "  -h, --help               Show this help message"
    echo
    echo "Example:"
    echo "  $0 -t 0.1.8-dev.31 -n emogi-app -p 8000 -e prod -i isakin/emogi-prod"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        -n|--name)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -e|--env)
            ENV="$2"
            shift 2
            ;;
        -i|--image)
            IMAGE_NAME="$2"
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
IMAGE_TAG=${IMAGE_TAG:-$DEFAULT_IMAGE_TAG}
CONTAINER_NAME=${CONTAINER_NAME:-$DEFAULT_CONTAINER_NAME}
PORT=${PORT:-$DEFAULT_PORT}
ENV=${ENV:-$DEFAULT_ENV}
IMAGE_NAME=${IMAGE_NAME:-$DEFAULT_IMAGE_NAME}
ENV_TAG=${ENV_TAG:-$DEFAULT_ENV_TAG}
ENV_VALUE=${ENV_VALUE:-$DEFAULT_ENV_VALUE}
NAME_TAG=${NAME_TAG:-$DEFAULT_NAME_TAG}
NAME_VALUE=${NAME_VALUE:-$DEFAULT_NAME_VALUE}

# Find EC2 instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:${ENV_TAG},Values=${ENV_VALUE}" "Name=tag:${NAME_TAG},Values=${NAME_VALUE}" \
    --query "Reservations[0].Instances[0].InstanceId" \
    --output text)

# Commands to execute
read -r -d '' COMMANDS << EOF
echo "🚀 Starting Docker image update for ${CONTAINER_NAME} with tag ${IMAGE_TAG}..."

# Pull new image
sudo docker pull ${IMAGE_NAME}:${IMAGE_TAG}

# Stop and remove existing container (if exists)
sudo docker stop ${CONTAINER_NAME} 2>/dev/null || true
sudo docker rm ${CONTAINER_NAME} 2>/dev/null || true

# Run new container
sudo docker run -d \
    --name ${CONTAINER_NAME} \
    -e ENV=${ENV} \
    -v ~/.aws:/root/.aws \
    -p ${PORT}:${PORT} \
    --health-cmd='python -c "import urllib.request; urllib.request.urlopen(\"http://localhost:${PORT}/health\")"' \
    --health-interval=10s \
    --health-timeout=5s \
    --health-retries=5 \
    --health-start-period=20s \
    ${IMAGE_NAME}:${IMAGE_TAG}

# Clean up unused images
echo "🧹 Cleaning up unused Docker images..."
sudo docker image prune -f

# Check container status
echo "🔍 Checking container status:"
sudo docker ps -a | grep ${CONTAINER_NAME}
EOF

if [ -n "$INSTANCE_ID" ]; then
    echo "🎬 Starting command execution..."
    
    # Convert commands to JSON array
    COMMANDS_JSON=$(echo "$COMMANDS" | jq -R -s 'split("\n")[:-1]')
    
    # Execute command and store Command ID
    COMMAND_ID=$(aws ssm send-command \
        --instance-ids "$INSTANCE_ID" \
        --document-name "AWS-RunShellScript" \
        --parameters "{\"commands\": $COMMANDS_JSON}" \
        --output text \
        --query "Command.CommandId")
    
    echo "✅ Command sent successfully! (Command ID: $COMMAND_ID)"
    echo "📌 Checking execution status..."
    
    # Monitor command execution status
    while true; do
        STATUS=$(aws ssm list-command-invocations \
            --command-id "$COMMAND_ID" \
            --details \
            --query "CommandInvocations[0].Status" \
            --output text)
        
        if [ "$STATUS" == "Success" ]; then
            echo "✅ Command execution completed successfully!"
            
            # Show execution results without pager
            echo "📝 Execution results:"
            aws ssm get-command-invocation \
                --command-id "$COMMAND_ID" \
                --instance-id "$INSTANCE_ID" \
                --query "StandardOutputContent" \
                --output text | cat
            break
        elif [ "$STATUS" == "Failed" ] || [ "$STATUS" == "Cancelled" ] || [ "$STATUS" == "TimedOut" ]; then
            echo "❌ Command execution failed! (Status: $STATUS)"
            echo "⚠️ Error details:"
            aws ssm get-command-invocation \
                --command-id "$COMMAND_ID" \
                --instance-id "$INSTANCE_ID" \
                --query "StandardErrorContent" \
                --output text | cat
            exit 1
        fi
        
        echo "⏳ Still running... (Current status: $STATUS)"
        sleep 2
    done
else
    echo "❌ No server found!"
fi