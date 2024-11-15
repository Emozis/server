from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import AuthServiceDep, CurrentUser
from app.schemas import LoginRequest, LoginGoogleRequest, UserCreate


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

@router.post(
    path="/login",
    description="email과 password를 사용하여 로그인합니다."
    )
@handle_exceptions
async def login(request: LoginRequest, auth_service: AuthServiceDep):
    return auth_service.login_id_password(request)

@router.post(
    path="/login/google/id-token",
    description="구글 로그인시 발급되는 id-token을 사용하여 인증합니다."
    )
@handle_exceptions
async def login_goole(request: LoginGoogleRequest, auth_service: AuthServiceDep):
    return auth_service.login_google(request.id_token)

@router.post(
    path="/token/test",
    description="테스트용 access-token을 반환합니다."
    )
async def login_test(auth_service: AuthServiceDep):
    response = auth_service.login_test()
    return response.access_token

@router.get(
    path="/token",
    description="발급된 access-token에서 사용자 정보를 반환합니다."
    )
async def get_user_info_from_token(user_id: CurrentUser, auth_service: AuthServiceDep):
    return {"user_id": user_id, "message": "This is a protected route"}