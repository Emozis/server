from fastapi import FastAPI
from contextlib import asynccontextmanager
import signal, os

from . import Settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        settings = Settings.load_and_validate()
        app.state.settings = settings
        
        yield
    except:
        os.kill(os.getpid(), signal.SIGTERM)
