from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..database import db_manager
from .dependencies import room_manager
from ..utils.constants import constants

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager.drop_all_tables(confirmation=True)
    db_manager.create_all_tables()
    db_manager.execute_sql_files(constants.SQL_FOLDER_PATH)

    yield

    await room_manager.shutdown()
