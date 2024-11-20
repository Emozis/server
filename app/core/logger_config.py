import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger().disabled = True
logger = logging.getLogger("uvicorn.info")
