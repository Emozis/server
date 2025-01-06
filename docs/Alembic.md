# Alembic 기본 명령어 정리

## 초기 설정
```bash
# alembic 초기화
poetry run alembic init alembic
```

## 마이그레이션 관련
```bash
# 새 마이그레이션 파일 생성 (모델 변경사항 자동 감지)
poetry run alembic revision --autogenerate -m "변경사항 설명"

# 마이그레이션 실행 (최신 버전으로)
poetry run alembic upgrade head

# 특정 버전으로 마이그레이션
poetry run alembic upgrade {revision_id}

# 이전 버전으로 롤백
poetry run alembic downgrade -1

# 처음 버전으로 롤백
poetry run alembic downgrade base
```

## 상태 확인
```bash
# 현재 적용된 마이그레이션 버전 확인
poetry run alembic current

# 마이그레이션 이력 조회
poetry run alembic history
```