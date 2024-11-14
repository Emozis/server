from typing import Generator
from sqlalchemy.orm import Session

from ..database import DatabaseManager

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