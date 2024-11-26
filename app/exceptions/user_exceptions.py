from .base_exception import BaseException


class UserConflictException(BaseException):
    def __init__(self, user_email: str):
        super().__init__(
            status_code=409,
            message="이미 존재하는 이메일입니다.",
            code="EMAIL_CONFLICT",
            data={"email": user_email}
        )
