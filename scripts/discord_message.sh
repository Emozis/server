#!/bin/bash

# Parameters
REPOSITORY=$1
BRANCH=$2
VERSION=$3
COMMIT_MESSAGE=$4
TEST_STATUS=$5
BUILD_STATUS=$6
DEPLOY_STATUS=$7
HEALTH_STATUS=$8
TIMESTAMP=$9

# Set color based on all statuses
if [[ "$BUILD_STATUS" == "success" ]] && [[ "$DEPLOY_STATUS" == "success" ]] && [[ "$HEALTH_STATUS" == "success" ]]; then
    if [[ -z "$TEST_STATUS" ]] || [[ "$TEST_STATUS" == "success" ]]; then
        COLOR="5763719"  # Green
    else
        COLOR="15548997"  # Red
    fi
else
    COLOR="15548997"  # Red
fi

# Convert statuses to emojis with Korean text
if [[ -z "$TEST_STATUS" ]]; then
    TEST_EMOJI="➖ 미실행"
else
    TEST_EMOJI=$([ "$TEST_STATUS" == "success" ] && echo "✅ 성공" || echo "❌ 실패")
fi

BUILD_EMOJI=$([ "$BUILD_STATUS" == "success" ] && echo "✅ 성공" || echo "❌ 실패")
DEPLOY_EMOJI=$([ "$DEPLOY_STATUS" == "success" ] && echo "✅ 성공" || echo "❌ 실패")
HEALTH_EMOJI=$([ "$HEALTH_STATUS" == "success" ] && echo "✅ 성공" || echo "❌ 실패")

# Create JSON output in a single line
echo "[{
    \"title\":\"🚀 ${REPOSITORY} 배포 결과\",
    \"description\":\"GitHub Actions 워크플로우 실행 결과\",
    \"color\":\"${COLOR}\",
    \"fields\":[
        {
            \"name\":\"저장소\",
            \"value\":\"${REPOSITORY}\",
            \"inline\":true
        },
        {
            \"name\":\"브랜치\",
            \"value\":\"\`${BRANCH}\`\",
            \"inline\":true
        },
        {
            \"name\":\"버전\",
            \"value\":\"\`${VERSION}\`\",
            \"inline\":true
        },
        {
            \"name\":\"커밋 메시지\",
            \"value\":\"${COMMIT_MESSAGE}\"
        },
        {
            \"name\":\"테스트 상태\",
            \"value\":\"${TEST_EMOJI}\"
        },
        {
            \"name\":\"빌드 상태\",
            \"value\":\"${BUILD_EMOJI}\"
        },
        {
            \"name\":\"배포 상태\",
            \"value\":\"${DEPLOY_EMOJI}\"
        },
        {
            \"name\":\"헬스 체크\",
            \"value\":\"${HEALTH_EMOJI}\"
        }
    ],
    \"footer\":{\"text\":\"GitHub Actions\"},
    \"timestamp\":\"${TIMESTAMP}\"
}]" | tr -d '\n' | sed 's/[[:space:]]\+/ /g'