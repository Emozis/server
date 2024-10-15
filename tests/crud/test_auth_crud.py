import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models import users as models
from app.schemas import user as schemas
from app.crud import auth_crud
from app.db import db

# 인메모리 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 테스트용 DB 세션 의존성
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[db.get_db] = override_get_db

# FastAPI 클라이언트 생성
client = TestClient(app)

# 테스트 전용 DB 테이블 생성
@pytest.fixture(autouse=True)
def create_test_db():
    db.Base.metadata.create_all(bind=engine)
    yield
    db.Base.metadata.drop_all(bind=engine)

# 실제 create_user 함수 테스트
def test_create_user():
    # 테스트용 유저 데이터 생성
    user_data = schemas.UserCreate(
        user_email="testuser@example.com",
        user_password="testpassword123",
        user_name="Test User",
        user_profile="Test Profile"
    )
    
    db = TestingSessionLocal()
    
    # CRUD 함수 실행
    created_user = auth_crud.create_user(user=user_data, db=db)

    # 결과 검증
    assert created_user.user_email == user_data.user_email
    assert created_user.user_password == user_data.user_password
    assert created_user.user_name == user_data.user_name
    assert created_user.user_profile == user_data.user_profile

    # DB에 유저가 정상적으로 저장되었는지 확인
    db_user = db.query(models.User).filter(models.User.user_email == user_data.user_email).first()
    assert db_user is not None
    assert db_user.user_email == user_data.user_email
