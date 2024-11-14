from functools import wraps
from fastapi import HTTPException

from . import logger
from ..exceptions import InternalServerError

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"❌ Internal server error: {str(e)}")
            raise InternalServerError(e)
    return wrapper