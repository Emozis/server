from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import AuthenticatedUser, UserServiceDep
from app.schemas import (
    UserUpdate, 
    UserResponse, 
    ErrorResponse, 
    ResponseSchema, 
    UserIdResponse,
    UserCreate
)


router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

@router.get(
    path="/me",
    description="현재 로그인된 유저 정보를 조회합니다.",
    responses={
        200: {"model": UserResponse, "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def read_user_by_id(user_id: AuthenticatedUser, user_service: UserServiceDep) -> UserResponse:
    return user_service.get_user_by_id(user_id)

@router.put(
    path="/me",
    description="현재 로그인된 유저 정보를 업데이트합니다.",
    responses={
        200: {"model": ResponseSchema[UserIdResponse], "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def update_user(user_id: AuthenticatedUser, user: UserUpdate, user_service: UserServiceDep) -> ResponseSchema:
    return user_service.update_user(user_id, user)

@router.patch(
    path="/me/deactivate",
    description="현재 로그인된 유저를 비활성화합니다.(탈퇴)",
    responses={
        200: {"model": ResponseSchema[UserIdResponse], "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def deactivate_user(user_id: AuthenticatedUser, user_service: UserServiceDep) -> ResponseSchema:
    """사용자 비활성화 엔드포인트"""
    return user_service.deactivate_user_by_id(user_id)