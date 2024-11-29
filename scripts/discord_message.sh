#!/bin/bash

# 매개변수
REPOSITORY=$1
BRANCH=$2
VERSION=$3
COMMIT_MESSAGE=$4
BUILD_STATUS=$5
DEPLOY_STATUS=$6
TIMESTAMP=$7

# 색상 설정 (성공: 녹색, 실패: 빨간색)
if [[ "$BUILD_STATUS" == "success" ]] && [[ "$DEPLOY_STATUS" == "success" ]]; then
    COLOR="5763719"
else
    COLOR="15548997"
fi

# BUILD_STATUS와 DEPLOY_STATUS를 이모지로 변환
BUILD_EMOJI=$([ "$BUILD_STATUS" == "success" ] && echo "✅ 성공" || echo "❌ 실패")
DEPLOY_EMOJI=$([ "$DEPLOY_STATUS" == "success" ] && echo "✅ 성공" || echo "❌ 실패")

# JSON을 단일 라인으로 출력
echo "[{\"title\":\"🚀 ${REPOSITORY} 배포 결과\",\"description\":\"GitHub Actions 워크플로우 실행 결과\",\"color\":\"${COLOR}\",\"fields\":[{\"name\":\"저장소\",\"value\":\"${REPOSITORY}\",\"inline\":true},{\"name\":\"브랜치\",\"value\":\"\`${BRANCH}\`\",\"inline\":true},{\"name\":\"버전\",\"value\":\"\`${VERSION}\`\",\"inline\":true},{\"name\":\"커밋 메시지\",\"value\":\"${COMMIT_MESSAGE}\"},{\"name\":\"빌드 상태\",\"value\":\"${BUILD_EMOJI}\"},{\"name\":\"배포 상태\",\"value\":\"${DEPLOY_EMOJI}\"}],\"footer\":{\"text\":\"GitHub Actions\"},\"timestamp\":\"${TIMESTAMP}\"}]"