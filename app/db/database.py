from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# SQLAlchemy 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# SessionMaker 생성
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Base 클래스 선언
Base = declarative_base()

# 예시 모델
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
