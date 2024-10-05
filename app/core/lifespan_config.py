from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()

        yield
    except Exception as e:
        print(f"Error during startup: {e}")