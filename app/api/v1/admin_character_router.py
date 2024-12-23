from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import CharacterServiceDep, AdminUser
from app.schemas import (
    CharacterResponse, 
    ErrorResponse,
)


router = APIRouter(
    prefix="/api/v1/admin/character",
    tags=["Character"]
)

@router.get(
    path="/all",
    description="모든 캐릭터를 조회하는 API입니다.",
    responses={
        200: {"model": list[CharacterResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_all_characters(admin_id: AdminUser, chararter_service: CharacterServiceDep) -> list[CharacterResponse]:
    return chararter_service.get_public_characters()
