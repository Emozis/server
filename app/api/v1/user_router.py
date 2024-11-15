from fastapi import APIRouter

from app.core import handle_exceptions, UserServiceDep
from app.schemas import UserCreate, UserUpdate, UserResponse, ErrorResponse, MessageResponse


router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

@router.post(
        path="/",
        responses={
            200: {"model": UserResponse, "description": "Successful Response"},
            409: {"model": ErrorResponse, "description": "User already exists"},
            500: {"model": ErrorResponse, "description": "Internal server error"}
        }
        )
@handle_exceptions
async def create_user(user: UserCreate, user_service: UserServiceDep):
    """새로운 유저 생성 엔드포인트"""
    user = user_service.create_user(user)
    return user

@router.get(
        path="/{user_id}",
        responses={
            200: {"model": UserResponse, "description": "Successful Response"},
            404: {"model": ErrorResponse, "description": "User not found"},
            500: {"model": ErrorResponse, "description": "Internal server error"}
        }
    )
@handle_exceptions
async def read_user_by_id(user_id: int, user_service: UserServiceDep):
    return user_service.get_user_by_id(user_id)

@router.get(
        path="/email/{user_email}",
        responses={
            200: {"model": UserResponse, "description": "Successful Response"},
            404: {"model": ErrorResponse, "description": "User not found"},
            500: {"model": ErrorResponse, "description": "Internal server error"}
        }
    )
@handle_exceptions
async def read_user_by_email(user_email: str, user_service: UserServiceDep):
    return user_service.get_user_by_email(user_email)

@router.put(
        path="/{user_id}",
        responses={
            200: {"model": UserResponse, "description": "Successful Response"},
            500: {"model": ErrorResponse, "description": "Internal server error"}
        }
    )
@handle_exceptions
async def update_user(user_id: int, user: UserUpdate, user_service: UserServiceDep):
    return user_service.update_user(user_id, user)

@router.delete(
    path="/{user_id}",
    responses={
        200: {"model": bool, "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def delete_user(user_id: int, user_service: UserServiceDep):
    """사용자 삭제 엔드포인트"""
    return user_service.delete_user_by_id(user_id)

@router.patch(
    path="/{user_id}/deactivate",
    responses={
        200: {"model": UserResponse, "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def deactivate_user(user_id: int, user_service: UserServiceDep):
    """사용자 비활성화 엔드포인트"""
    return user_service.deactivate_user_by_id(user_id)