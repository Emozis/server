from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..core import constants
from .dependencies import db_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager.drop_all_tables(confirmation=True)
    db_manager.create_all_tables()
    db_manager.execute_sql_files(constants.SQL_FOLDER_PATH)

    yield
