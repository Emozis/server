from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from . import engine, AsyncSessionLocal, Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
