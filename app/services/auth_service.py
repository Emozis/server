from sqlalchemy.orm import Session

from ..core import logger
from ..crud import UserCRUD
from ..schemas import UserCreate, UserResponse, LoginRequest, LoginResponse
from ..utils import decode_id_token, JwtUtil, password_hasher
from ..models import User
from ..mappers import UserMapper
from ..exceptions import auth_exceptions, user_exceptions


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_crud = UserCRUD(db)

    def _signin(self, user: UserCreate) -> UserResponse:
        """
        신규 사용자 회원가입 처리
        Args:
            user (UserCreate): 생성할 사용자 정보
        Returns:
            UserResponse: 생성된 사용자 정보
        Raises:
            UserAlreadyExistsException: 이미 존재하는 이메일인 경우
        """
        existing_user = self.user_crud.get_user_by_email(user.user_email)
        if existing_user and existing_user.user_is_active:
            raise auth_exceptions.UserAlreadyExistsException(existing_user.user_email)
        
        # 비밀번호 해시화
        if user.user_password:
            user.user_password = password_hasher.hash_password(user.user_password)
        else:
            # 소셜 로그인의 경우 임의의 안전한 비밀번호 생성
            import secrets
            import string
            alphabet = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(16))
            user.user_password = password_hasher.hash_password(temp_password)

        db_user = self.user_crud.create(UserMapper.user_create_to_model(user))
        logger.info(f"✅ successfully sign in - id: {db_user.user_id}, name: {db_user.user_name}, email: {db_user.user_email}")

        return UserMapper.to_dto(db_user)
    
    def _make_auth_respone(self, status: str, message: str, user: User):
        """
        인증 응답 생성
        Args:
            status (str): 인증 상태 ("success" 또는 "registration")
            message (str): 응답 메시지
            user (User): 사용자 정보
        Returns:
            LoginResponse: 인증 응답 (상태, 메시지, 사용자 정보, 액세스 토큰 포함)
        """
        response = {
            "status": status,
            "message": message,
            "user": {
                "user_id": user.user_id,
                "user_email": user.user_email,
                "user_name": user.user_name,
                "user_profile": user.user_profile
            },
            "access_token": JwtUtil.create_access_token(user.user_id, user.user_name)
        }
        return LoginResponse(**response)
    
    def _login(self, user: UserCreate) -> LoginResponse:
        """
        로그인 또는 회원가입 처리
        Args:
            user (UserCreate): 로그인할 사용자 정보
        Returns:
            LoginResponse: 로그인 응답 정보
        """
        existing_user = self.user_crud.get_active_user_by_email(user.user_email)
        if existing_user:
            user = existing_user
            status = "success"
            message = "로그인에 성공하였습니다."
        else:
            user = self._signin(user)
            status = "registration"
            message = "신규 회원가입 및 로그인에 성공하였습니다."

        logger.info(f"✅ login complete! - id: {user.user_id}, name: {user.user_name}")
        return self._make_auth_respone(status, message, user)
    
    def login_id_password(self, request: LoginRequest) -> LoginResponse:
        """
        이메일/비밀번호 로그인 처리
        Args:
            request (LoginRequest): 로그인 요청 정보 (이메일, 비밀번호)
        Returns:
            LoginResponse: 로그인 응답 정보
        Raises:
            UserNotFoundException: 사용자를 찾을 수 없는 경우
            InvalidPasswordException: 비밀번호가 일치하지 않는 경우
        """
        existing_user = self.user_crud.get_active_user_by_email(request.user_email)
        if not existing_user:
            raise user_exceptions.UserNotFoundException(user_email=request.user_email)
        
        if not password_hasher.verify_password(request.user_password, existing_user.user_password):
            raise auth_exceptions.InvalidPasswordException()

        return self._make_auth_respone(status="success", message="로그인에 성공하였습니다.", user=existing_user)
    
    def login_google(self, id_token: str) -> LoginResponse:
        """
        구글 소셜 로그인 처리
        Args:
            id_token (str): 구글 ID 토큰
        Returns:
            LoginResponse: 로그인 응답 정보
        Raises:
            InvalidGoogleTokenException: 유효하지 않은 구글 토큰인 경우
        """
        google_user = decode_id_token(id_token)
        if not google_user:
            raise auth_exceptions.InvalidGoogleTokenException(id_token)
        
        return self._login(google_user)
    
    def login_test(self) -> LoginResponse:
        """
        테스트용 로그인 처리
        Returns:
            LoginResponse: 테스트 계정의 로그인 응답 정보
        """
        test_user = UserCreate(user_email="test@example.com", user_password="test", user_name="Test User", user_profile="test.jpg")
        return self._login(test_user)
    
    def decode_token(self, token: str) -> int:
        """
        JWT 토큰 검증 및 디코딩
        Args:
            token (str): 검증할 JWT 토큰
        Returns:
            int: 토큰에서 추출한 사용자 ID
        Raises:
            JWTDecodeError: 토큰이 유효하지 않은 경우
        """
        return JwtUtil.verify_token(token)