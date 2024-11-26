from fastapi import HTTPException
from datetime import datetime

class BaseException(HTTPException):
    def __init__(
        self, 
        status_code: int,
        message: str,
        code: str,
        data: dict = None,
        headers: dict = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "code": code,
                "timestamp": datetime.now().isoformat(),
                **(data or {})
            },
            headers=headers
        )