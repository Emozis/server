from sqlalchemy.orm import Session
from jose.exceptions import JWTError
from jwt import PyJWKClient
import jwt

from ..core import logger, settings
from ..crud import UserCRUD
from ..schemas import UserCreate, UserResponse, LoginRequest, LoginResponse
from ..utils.jwt_util import JwtUtil
from ..utils.password_hasher import password_hasher
from ..models import User
from ..mappers import UserMapper
from ..exceptions import NotFoundException
from ..exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordException,
    InvalidGoogleTokenException
)


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
            raise UserAlreadyExistsException(existing_user.user_email)
        
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
    
    def _make_auth_respone(self, status: str, message: str, user: User, role: str = "user") -> LoginResponse:
        """
        인증 응답 생성
        Args:
            status (str): 인증 상태 ("success" 또는 "registration")
            message (str): 응답 메시지
            role (str): 사용자 종류
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
            "access_token": JwtUtil.create_access_token(user.user_id, user.user_name, role)
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

    def _decode_id_token(self, id_token: str) -> UserCreate:
        """
        Google ID 토큰을 디코딩하여 사용자 정보를 추출합니다.
        Google의 공개 키를 사용하여 토큰을 검증하고, 토큰에 포함된 사용자 정보를 UserCreate 객체로 변환합니다.
        
        Args:
            id_token (str): Google에서 발급받은 ID 토큰
            
        Returns:
            UserCreate: 디코딩된 사용자 정보를 담은 객체. 토큰이 유효하지 않은 경우 None 반환
            
        Raises:
            JWTError: 토큰 디코딩 또는 검증 과정에서 오류가 발생한 경우
        """
        jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
        jwks_client = PyJWKClient(jwks_url)

        signing_key = jwks_client.get_signing_key_from_jwt(id_token)

        options = {
            'verify_iat': True
        }

        try:
            user_info: dict = jwt.decode(id_token, signing_key.key, algorithms=["RS256"], audience=settings.GOOGLE_CLIENT_ID, options=options, leeway=30)
        except JWTError as e:
            logger.error(f"❌ JWT decoding error: {e}")
            return None
        
        user_data = {
            "user_id": int(user_info.get("sub")),
            "user_email": user_info.get("email"),
            "user_name": user_info.get("name"),
            "user_profile": user_info.get("picture"),
        }
        user = UserCreate(**user_data)
        return user
    
    def login_id_password(self, request: LoginRequest) -> LoginResponse:
        """
        이메일/비밀번호 로그인 처리
        Args:
            request (LoginRequest): 로그인 요청 정보 (이메일, 비밀번호)
        Returns:
            LoginResponse: 로그인 응답 정보
        Raises:
            NotFoundException: 사용자를 찾을 수 없는 경우
            InvalidPasswordException: 비밀번호가 일치하지 않는 경우
        """
        existing_user = self.user_crud.get_active_user_by_email(request.user_email)
        if not existing_user:
            raise NotFoundException("사용자를 찾을 수 없습니다.", "user_email", request.user_email)
        
        if not password_hasher.verify_password(request.user_password, existing_user.user_password):
            raise InvalidPasswordException()

        return self._make_auth_respone(status="success", message="로그인에 성공하였습니다.", role=existing_user.user_role.value, user=existing_user)
    
    def login_admin(self, request: LoginRequest) -> LoginResponse:
        """
        관리자 계정 로그인 처리
        Args:
            request (LoginRequest): 로그인 요청 정보 (이메일, 비밀번호)
        Returns:
            LoginResponse: 로그인 응답 정보
        Raises:
            NotFoundException: 관리자 권한을 가진 사용자를 찾을 수 없는 경우
            InvalidPasswordException: 비밀번호가 일치하지 않는 경우
        """
        existing_user = self.user_crud.get_admin_user_by_email_and_role(request.user_email)
        if not existing_user:
            raise NotFoundException("사용자를 찾을 수 없습니다.", "user_email", request.user_email)
        
        if not password_hasher.verify_password(request.user_password, existing_user.user_password):
            raise InvalidPasswordException()

        return self._make_auth_respone(status="success", message="로그인에 성공하였습니다.", role=existing_user.user_role.value, user=existing_user)
    
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
        google_user = self._decode_id_token(id_token)
        if not google_user:
            raise InvalidGoogleTokenException(id_token)
        
        return self._login(google_user)
    
    def login_test(self) -> LoginResponse:
        """
        테스트용 로그인 처리
        Returns:
            LoginResponse: 테스트 계정의 로그인 응답 정보
        """
        test_user = UserCreate(user_email="test@example.com", user_password="test", user_name="Test User", user_profile="test.jpg")
        return self._login(test_user)