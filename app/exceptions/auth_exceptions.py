from .base_exception import BaseException

class InvalidTokenException(BaseException):
    def __init__(self, token: str = None, message: str = None):
        details = {"token": token} if token else {}
        super().__init__(
            status_code=401,
            message= message if message else "유효하지 않은 인증 정보입니다.",
            code="INVALID_TOKEN",
            headers={"WWW-Authenticate": "Bearer"},
            details=details
        )

class InvalidPasswordException(BaseException):
    def __init__(self, email: str = None):
        details = {"email": email} if email else {}
        super().__init__(
            status_code=401,
            message="비밀번호가 일치하지 않습니다.",
            code="INVALID_PASSWORD",
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