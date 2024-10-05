from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..core import constants
from ..db import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.create_database()
        await db.clear_all_tables()
        await db.init_db()
        await db.execute_sql_file(constants.SQL_FOLDER_PATH)

        yield
    except Exception as e:
        print(f"Error during startup: {e}")