from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..db import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.create_database()
        await db.init_db()
        await db.execute_sql_file()

        yield
    except Exception as e:
        print(f"Error during startup: {e}")