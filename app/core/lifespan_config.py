from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..core import settings
from ..database.database_manager import db_manager
from .dependencies import room_manager
from ..utils.constants import constants

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DROP_ALL_TABLES:
        db_manager.drop_all_tables(confirmation=True)
        db_manager.create_all_tables()
        db_manager.execute_sql_files(constants.SQL_FOLDER_PATH)

    yield

    await room_manager.shutdown()
