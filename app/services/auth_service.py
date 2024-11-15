from sqlalchemy.orm import Session

from ..core import logger
from ..crud import UserCRUD
from ..schemas import UserCreate, UserResponse, LoginResponse
from ..utils import decode_id_token, JwtUtil
from ..mappers import UserMapper
from ..exceptions import auth_exceptions
from .user_service import UserService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_crud = UserCRUD(db)
        self.user_service = UserService(db)

    def _signin_google(self, user: UserCreate) -> UserResponse:
        existing_user = self.user_service.get_user_by_email(user.user_email)
        if existing_user:
            raise auth_exceptions.UserAlreadyExistsException(existing_user.user_email)
        
        user = UserMapper.to_dto(self.user_crud.create(user))
        logger.info(f"✅ successfully sign in - id: {user.user_id}, name: {user.user_name}, email: {user.user_email}")

        return user
    
    def _login(self, user: UserCreate) -> LoginResponse:
        existing_user = self.user_service.get_user_by_email(user.user_email)
        if existing_user:
            user = existing_user
            status = "success"
            message = "로그인에 성공하였습니다."
        else:
            user = self._signin_google(user)
            status = "registration"
            message = "신규 회원가입 및 로그인에 성공하였습니다."

        logger.info(f"✅ login complete! - id: {user.user_id}, name: {user.user_name}")

        response = {
            "status": status,
            "message": message,
            "user": {
                "user_id": user.user_id,
                "user_email": user.user_email,
                "user_name": user.user_name,
                "user_profile": user.user_profile
            },
            "access_token": JwtUtil.create_access_token(user.user_id)
        }
        return LoginResponse(**response)
    
    def login_google(self, id_token: str) -> LoginResponse:
        google_user = decode_id_token(id_token)
        if not google_user:
            raise auth_exceptions.InvalidGoogleTokenException(id_token)
        
        return self._login(google_user)
    
    def login_test(self) -> LoginResponse:
        test_user = UserCreate(user_email="test@example.com", user_password="test", user_name="Test User", user_profile="test.jpg")
        return self._login(test_user)
    
    def decode_token(self, token: str) -> int:
        return JwtUtil.verify_token(token)