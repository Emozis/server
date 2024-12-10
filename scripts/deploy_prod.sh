#!/bin/bash

# 매개변수
PROJECT_PATH=$1
DOCKER_USERNAME=$2
IMAGE_NAME=$3
VERSION=$4
CONTAINER_NAME=$5

# 프로젝트 디렉토리 생성
mkdir -p $PROJECT_PATH

sudo docker pull "${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

sudo docker stop "${CONTAINER_NAME}" | true

sudo docker rm "${CONTAINER_NAME}" | true

sudo docker run -d \
  --name "${CONTAINER_NAME}" \
  -v ${PROJECT_PATH}/.env.dev:/app/.env.dev \
  -v ~/.aws:/root/.aws \
  -p 8000:8000 \
  --health-cmd='python -c "import urllib.request; urllib.request.urlopen(\"http://localhost:8000/health\")"' \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=5 \
  --health-start-period=20s \
  "${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"