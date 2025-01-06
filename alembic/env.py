# alembic/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Base만 직접 import
from app.database.base import Base
from app.core.settings import settings

# this is the Alembic Config object
config = context.config

# DB URL 설정
config.set_main_option("sqlalchemy.url", settings.POSTGRES_HOST)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata