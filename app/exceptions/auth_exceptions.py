from .base_exception import BaseException

class InvalidTokenException(BaseException):
    def __init__(self, token: str = None, message: str = None):
        data = {"token": token} if token else {}
        super().__init__(
            status_code=401,
            message= message if message else "유효하지 않은 인증 정보입니다.",
            code="INVALID_TOKEN",
            headers={"WWW-Authenticate": "Bearer"},
            data=data
        )

class InvalidPasswordException(BaseException):
    def __init__(self, email: str = None):
        data = {"email": email} if email else {}
        super().__init__(
            status_code=401,
            message="비밀번호가 일치하지 않습니다.",
            code="INVALID_PASSWORD",
            data=data
        )

class InvalidGoogleTokenException(BaseException):
    def __init__(self, token: str = None):
        data = {"token": token} if token else {}
        data["auth_provider"] = "google"
        
        super().__init__(
            status_code=401,
            message="유효하지 않은 Google 인증 토큰입니다.",
            code="INVALID_GOOGLE_TOKEN",
            data=data
        )
        
class UserAlreadyExistsException(BaseException):
    def __init__(self, email: str):
        super().__init__(
            status_code=409,
            message="이미 가입된 사용자입니다.",
            code="USER_EXISTS",
            data={
                "email": email
            }
        )

class UnauthorizedException(BaseException):
    def __init__(self, message: str = "접근 권한이 없습니다."):
        super().__init__(
            status_code=403,
            message=message,
            code="UNAUTHORIZED",
            data={}
        )