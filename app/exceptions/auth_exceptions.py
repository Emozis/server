from .base_exception import BaseException

class InvalidTokenException(BaseException):
    def __init__(self, token: str = None):
        details = {"token": token} if token else {}
        super().__init__(
            status_code=401,
            message="유효하지 않은 인증 토큰입니다.",
            code="INVALID_TOKEN",
            details=details
        )

class InvalidGoogleTokenException(BaseException):
    def __init__(self, token: str = None):
        details = {"token": token} if token else {}
        details["auth_provider"] = "google"
        
        super().__init__(
            status_code=401,
            message="유효하지 않은 Google 인증 토큰입니다.",
            code="INVALID_GOOGLE_TOKEN",
            details=details
        )
        
class UserAlreadyExistsException(BaseException):
    def __init__(self, email: str):
        super().__init__(
            status_code=409,
            message="이미 가입된 사용자입니다.",
            code="USER_EXISTS",
            details={
                "email": email
            }
        )