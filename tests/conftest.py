import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.dependencies import get_db
from tests.database.database_manager import DatabaseManagerForTest

@pytest.fixture(scope="session")
def db_manager():
    """테스트 데이터베이스 매니저"""
    manager = DatabaseManagerForTest()
    manager.create_database()
    manager.setup_database()
    
    yield manager
    
    # 테스트 완료 후 데이터베이스 삭제
    # manager.drop_database()

@pytest.fixture(scope="function")
def db_session(db_manager):
    """테스트용 데이터베이스 세션"""
    session = db_manager.SessionLocal()
    try:
        yield session
    finally:
        # session.rollback()  # 각 테스트 후 롤백
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """테스트 클라이언트"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client