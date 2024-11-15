from typing import Generator, Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import DatabaseManager
from ..services import UserService, AuthService

# 데이터베이스 매니저 인스턴스 생성
db_manager = DatabaseManager()
engine, SessionLocal, Base = db_manager.init_database()

def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션 제공"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]