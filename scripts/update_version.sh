#!/bin/bash

# 현재 버전 읽기
BASE_VERSION=$(cat pyproject.toml | grep version | head -n 1 | cut -d'"' -f2)

# 버전 파싱 및 증가
MAJOR=$(echo $BASE_VERSION | cut -d. -f1)
MINOR=$(echo $BASE_VERSION | cut -d. -f2)
PATCH=$(echo $BASE_VERSION | cut -d. -f3)

# PATCH 버전 증가
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="${MAJOR}.${MINOR}.${NEW_PATCH}"

if [[ "$1" == "refs/heads/main" ]]; then
    echo "version=${NEW_VERSION}" >> $GITHUB_OUTPUT
    sed -i "s/version = \"${BASE_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml
    
    git config --global user.name 'GitHub Actions'
    git config --global user.email 'actions@github.com'
    
    git add pyproject.toml
    git commit -m "chore: bump version to ${NEW_VERSION} [skip ci]"
    git push
else
    echo "version=${BASE_VERSION}-dev.${2}" >> $GITHUB_OUTPUT
fi