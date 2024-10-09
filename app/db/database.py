from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from pathlib import Path
import asyncpg

from ..core import settings, logger

class Database:
    def __init__(self):
        self.echo = False
        self.database_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}"
        self.engine = create_async_engine(self.database_url, echo=self.echo)
        self.AsyncSessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine, 
            class_=AsyncSession
        )
        self.Base = declarative_base()

    async def create_database(self):
        """데이터베이스가 없으면 새로운 데이터베이스를 생성하는 함수"""
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
        self.engine = create_async_engine(self.database_url, echo=self.echo)

    async def init_db(self):
        """모든 테이블을 생성하여 데이터베이스 초기화"""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)
    
    async def clear_all_tables(self):
        """모든 테이블의 데이터를 삭제하는 함수"""
        async with self.engine.begin() as conn:
            for table in reversed(self.Base.metadata.sorted_tables):
                await conn.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE"))
            logger.info("🗑️  Cleared all data from all tables.")

    async def execute_sql_file(self, sql_folder_path: str):
        """주어진 SQL 파일을 읽어 SQL 문을 실행하는 함수."""
        try:
            base_dir = Path.cwd()
            sql_folder_path = base_dir / sql_folder_path

            sql_files = list(sql_folder_path.glob('*.sql'))

            if any(sql_files):
                async with self.engine.begin() as conn:
                    for file_path in sql_files:
                        if file_path.exists():
                            sql_script = file_path.read_text(encoding='utf-8')

                            sql_statements = sql_script.split(';')

                            for statement in sql_statements:
                                statement = statement.strip()
                                if statement:
                                    await conn.execute(text(statement))
                                    logger.debug(f"Executed: {statement}")
                logger.info(f"✅ All SQL scripts in '{sql_folder_path}' executed successfully.")
            else:
                logger.warning(f"⚠️  No SQL files found in '{sql_folder_path}'.")
        except Exception as e:
            logger.warning(f"⚠️  Error executing SQL file: {str(e.orig).splitlines()[0]}")

    async def get_db(self):
        """데이터베이스 세션을 반환하는 함수"""
        async with self.AsyncSessionLocal() as session:
            yield session

db = Database()