from functools import wraps
from fastapi import HTTPException
import traceback

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
            error_detail = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'traceback': traceback.format_exc()
            }
            logger.error(
                f"❌ Internal server error:\n"
                f"- Error Type: {error_detail['error_type']}\n"
                f"- Error Message: {error_detail['error_message']}\n"
                f"- Traceback:\n{error_detail['traceback']}"
            )
            raise InternalServerError(e)
    return wrapper