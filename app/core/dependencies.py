from typing import Generator, Annotated
from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from ..database import DatabaseManager
from ..services import UserService, AuthService, RelationshipService, DefaultImageService
from ..exceptions import InvalidTokenException
from ..utils import JwtUtil

db_manager = DatabaseManager()
engine, SessionLocal, Base = db_manager.init_database()

api_key_scheme = APIKeyHeader(
    name="Authorization",
    description="Bearer {test-token}. 테스트 토큰을 받으려면 /api/v1/auth/token/test를 먼저 호출하세요.",
    auto_error=False
)

def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션 제공"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(auth_header: str = Depends(api_key_scheme)) -> int:
    """현재 인증된 사용자의 ID를 반환하는 의존성 함수"""
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else auth_header
    if not token:
        raise InvalidTokenException(None, "인증 정보가 제공되지 않았습니다.")
    try:
        user_id = JwtUtil.verify_token(token)
        if not user_id:
            raise InvalidTokenException(token)
        return user_id
    except Exception as e:
        raise InvalidTokenException(token)
    
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_relationship_service(db: Session = Depends(get_db)) -> RelationshipService:
    return RelationshipService(db)

def get_default_image_service(db: Session = Depends(get_db)) -> DefaultImageService:
    return DefaultImageService(db)

CurrentUser = Annotated[int, Depends(get_current_user)]

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
RelationshipServiceDep = Annotated[RelationshipService, Depends(get_relationship_service)]
DefaultImageServiceDep = Annotated[DefaultImageService, Depends(get_default_image_service)]