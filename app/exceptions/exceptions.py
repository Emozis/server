from fastapi import HTTPException
from datetime import datetime

class CustomException(HTTPException):
    def __init__(
        self, 
        status_code: int,
        message: str,
        code: str,
        details: dict = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "code": code,
                "timestamp": datetime.now().isoformat(),
                "details": details
            }
        )

class UserNotFoundException(CustomException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            message="사용자를 찾을 수 없습니다.",
            code="USER_NOT_FOUND",
            details={"user_id": user_id}
        )

class InternalServerError(CustomException):
    def __init__(self, error: Exception):
        super().__init__(
            status_code=500,
            message="내부 서버 오류가 발생했습니다.",
            code="INTERNAL_SERVER_ERROR",
            details={"error": str(error)}
        )