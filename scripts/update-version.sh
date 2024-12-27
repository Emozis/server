#!/bin/bash

# 버전 업데이트 기본값 설정
VERSION_UP=false

# 명령행 인자 파싱
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --version-up)
            if [[ "$2" == "true" || "$2" == "false" ]]; then
                VERSION_UP=$2
                shift
            else
                echo "Error: --version-up requires true or false value"
                exit 1
            fi
            ;;
        *) PARAMS="$PARAMS $1" ;;
    esac
    shift
done

# PARAMS에서 필요한 인자 추출
set -- $PARAMS
BRANCH_REF=$1
RUN_NUMBER=$2

# 현재 버전 읽기
BASE_VERSION=$(cat pyproject.toml | grep version | head -n 1 | cut -d'"' -f2)

if [[ "$BRANCH_REF" == "refs/heads/main" ]]; then
    if [[ "$VERSION_UP" == "true" ]]; then
        # 버전 파싱 및 증가
        MAJOR=$(echo $BASE_VERSION | cut -d. -f1)
        MINOR=$(echo $BASE_VERSION | cut -d. -f2)
        PATCH=$(echo $BASE_VERSION | cut -d. -f3)
        
        # PATCH 버전 증가
        NEW_PATCH=$((PATCH + 1))
        NEW_VERSION="${MAJOR}.${MINOR}.${NEW_PATCH}"
        
        echo "version=${NEW_VERSION}" >> $GITHUB_OUTPUT
        sed -i "s/version = \"${BASE_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml
        
        git config --global user.name 'GitHub Actions'
        git config --global user.email 'actions@github.com'
        
        git add pyproject.toml
        git commit -m "[Chore]: bump version to ${NEW_VERSION} [skip ci]"
        git push
    else
        echo "version=${BASE_VERSION}" >> $GITHUB_OUTPUT
    fi
else
    echo "version=${BASE_VERSION}-dev.${RUN_NUMBER}" >> $GITHUB_OUTPUT
fi