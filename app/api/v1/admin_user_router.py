from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import AdminUser, UserServiceDep
from app.schemas import (
    UserResponse, 
    ErrorResponse
)


router = APIRouter(
    prefix="/api/v1/admin/user",
    tags=["User"]
)

@router.get(
    path="/all",
    description="모든 유저 정보를 조회합니다.",
    responses={
        200: {"model": list[UserResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def read_all_users(admin_id: AdminUser, user_service: UserServiceDep) -> list[UserResponse]:
    return user_service.get_all_users()