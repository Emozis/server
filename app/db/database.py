import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..core import settings, logger

class Database:
    def __init__(self):
        self.database_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}"
        self.engine = create_async_engine(self.database_url, echo=True)
        self.AsyncSessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine, 
            class_=AsyncSession
        )
        self.Base = declarative_base()

    async def create_database(self):
        db_name = settings.db_name
        conn = await asyncpg.connect(user=settings.db_user, password=settings.db_password, host=settings.db_host, port=settings.db_port, database='postgres')

        try:
            await conn.execute(f'CREATE DATABASE {db_name}')
            logger.info(f"⚙️  Database '{db_name}' has been created.")
        except asyncpg.exceptions.DuplicateDatabaseError:
            pass
        finally:
            await conn.close()

        self.database_url = f"{self.database_url}/{db_name}"
        self.engine = create_async_engine(self.database_url, echo=True)

    async def init_db(self):
        """Initialize the database by creating all tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def get_db(self):
        """Yield a database session."""
        async with self.AsyncSessionLocal() as session:
            yield session

# 사용 예시
db = Database()

# 새 데이터베이스를 생성하려면:
# await db.create_database("new_db_name")

# 테이블 생성 및 DB 초기화는:
# await db.init_db()

# FastAPI 핸들러에서 DB 세션을 사용하려면:
# async def some_route(db_session: AsyncSession = Depends(db.get_db)):
