from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import AuthServiceDep
from app.schemas import (
    LoginRequest, 
    LoginGoogleRequest, 
    ErrorResponse, 
    LoginResponse
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

@router.post(
    path="/login",
    description="email과 password를 사용하여 로그인합니다.",
    responses={
        200: {"model": LoginResponse, "description": "Successful Response"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def login(request: LoginRequest, auth_service: AuthServiceDep) -> LoginResponse:
    return auth_service.login_id_password(request)

@router.post(
    path="/login/google",
    description="구글 로그인시 발급되는 id-token을 사용하여 인증합니다.",
    responses={
        200: {"model": LoginResponse, "description": "Successful Response"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def login_goole(request: LoginGoogleRequest, auth_service: AuthServiceDep) -> LoginResponse:
    return auth_service.login_google(request.id_token)

@router.post(
    path="/login/test",
    description="테스트용 access-token을 반환합니다.",
    responses={
        200: {"model": LoginResponse, "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def login_test(auth_service: AuthServiceDep) -> LoginResponse:
    return auth_service.login_test()