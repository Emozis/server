#!/bin/bash

# 매개변수
PROJECT_PATH=$1
DOCKER_USERNAME=$2
IMAGE_NAME=$3
VERSION=$4

# 프로젝트 디렉토리 생성
mkdir -p $PROJECT_PATH

# docker-compose.yml 파일의 이미지 태그 업데이트
sed -i "s|image: ${DOCKER_USERNAME}/${IMAGE_NAME}:.*|image: ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}|" docker-compose.yml

# 컨테이너 업데이트 및 재시작
docker compose pull
docker compose up -d

# 사용하지 않는 Docker 이미지 정리
docker image prune -af