# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy import text

# class TestDatabase:
#     def __init__(self):
#         """테스트 환경에 맞게 SQLite in-memory 데이터베이스 설정"""
#         self.echo = False
#         self.database_url = "sqlite+aiosqlite:///:memory:"  # In-memory SQLite DB
#         self.engine = create_async_engine(self.database_url, echo=self.echo)
#         self.AsyncSessionLocal = sessionmaker(
#             autocommit=False, 
#             autoflush=False, 
#             bind=self.engine, 
#             class_=AsyncSession
#         )
#         self.TestBase = declarative_base()

#     async def init_db(self):
#         """테스트용 데이터베이스 초기화, 모든 테이블 생성"""
#         async with self.engine.begin() as conn:
#             await conn.run_sync(self.TestBase.metadata.create_all)
    
#     async def clear_all_tables(self):
#         """테스트 후 테이블을 모두 비우는 함수"""
#         async with self.engine.begin() as conn:
#             for table in reversed(self.TestBase.metadata.sorted_tables):
#                 await conn.execute(text(f"DELETE FROM {table.name}"))
#             await conn.commit()

#     async def get_db(self):
#         """테스트용 데이터베이스 세션을 반환하는 함수"""
#         async with self.AsyncSessionLocal() as session:
#             yield session

# test_db = TestDatabase()