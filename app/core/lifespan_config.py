from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..core import logger, settings, ProdConfig
from ..database.database_manager import db_manager
from .dependencies import room_manager
from ..utils.constants import constants

@asynccontextmanager
async def lifespan(app: FastAPI):
    env = "prod" if isinstance(settings, ProdConfig) else "dev"
    # env_emoji = "🚀" if env == "prod" else "🛠️ "

    if settings.DROP_ALL_TABLES:
        db_manager.drop_all_tables(confirmation=True)
        db_manager.create_all_tables()
        db_manager.execute_sql_files(constants.SQL_FOLDER_PATH)

    # logger.info(f"{env_emoji} Server is ready! Environment: {env.upper()} ✨")

    yield

    logger.info("🔄 Shutting down server...")
    await room_manager.shutdown()
    logger.info("👋 Server shutdown complete")
