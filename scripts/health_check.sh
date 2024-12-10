#!/bin/bash

# Parameters
PROJECT_PATH=$1

# Load environment variables
source "${PROJECT_PATH}/.env"

# Set default port if SERVER_PORT is not set
: "${SERVER_PORT:=8000}"    

attempts=0
max_attempts=10

echo "Starting health check on port ${SERVER_PORT}..."

until curl -sf "http://localhost:${SERVER_PORT}/health" || [ $attempts -eq $max_attempts ]
do
    attempts=$((attempts+1))
    echo "Health check attempt $attempts of $max_attempts..."
    sleep 15
done

if [ $attempts -eq $max_attempts ]; then
    echo "Health check failed after $max_attempts attempts"
    exit 1
fi

echo "Application is healthy!"