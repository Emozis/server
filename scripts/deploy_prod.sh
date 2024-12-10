#!/bin/bash

# 매개변수
PROJECT_PATH=$1
DOCKER_USERNAME=$2
IMAGE_NAME=$3
VERSION=$4

# 프로젝트 디렉토리 생성
mkdir -p $PROJECT_PATH

docker pull "${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"