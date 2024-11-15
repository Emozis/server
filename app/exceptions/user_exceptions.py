from .base_exception import BaseException

class UserNotFoundException(BaseException):
    def __init__(self, user_id: int = None, user_email: str = None):
        super().__init__(
            status_code=404,
            message="사용자를 찾을 수 없습니다.",
            code="USER_NOT_FOUND",
            details={"user_id": user_id, "user_email": user_email}
        )

class UserConflictException(BaseException):
    def __init__(self, user_email: str):
        super().__init__(
            status_code=409,
            message="이미 존재하는 이메일입니다.",
            code="EMAIL_CONFLICT",
            details={"email": user_email}
        )

class InternalServerError(BaseException):
    def __init__(self, error: Exception):
        super().__init__(
            status_code=500,
            message="내부 서버 오류가 발생했습니다.",
            code="INTERNAL_SERVER_ERROR",
            details={"error": str(error)}
        )