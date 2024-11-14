from fastapi import APIRouter, Depends, HTTPException

from app.core import handle_exceptions, UserServiceDep
from app.schemas import UserCreate, ErrorResponse


router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

@router.post("/")
@handle_exceptions
async def create_users(user: UserCreate, user_service: UserServiceDep):
    """새로운 유저 생성 엔드포인트"""
    user = user_service.create_user(user)
    return user

@router.get(
        path="/{user_id}",
        responses={
            404: {"model": ErrorResponse, "description": "User not found"},
            500: {"model": ErrorResponse, "description": "Internal server error"}
        }
    )
@handle_exceptions
async def read_users(user_id: int, user_service: UserServiceDep):
    return user_service.get_user_id(user_id)