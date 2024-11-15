from fastapi import APIRouter

from app.core import handle_exceptions, AuthServiceDep
from app.schemas import LoginGoogleIdToken


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

@router.post(
    path="/login/google/id-token",
    description="구글 로그인시 발급되는 id-token을 사용하여 인증합니다."
    )
@handle_exceptions
async def login_goole(data: LoginGoogleIdToken, auth_service: AuthServiceDep):
    return auth_service.login_google(data.id_token)

@router.post(
    path="/token/test",
    description="테스트용 access-token을 반환합니다."
    )
async def login_test(auth_service: AuthServiceDep):
    return auth_service.login_test()

@router.get(
    path="/token",
    description="발급된 access-token에서 사용자 정보를 반환합니다."
    )
async def get_user_info_from_token(auth_service: AuthServiceDep):
    auth_service.decode_token()
    return {"user_id": "aaaa", "message": "This is a protected route"}