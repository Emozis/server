from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import CharacterServiceDep, AdminUser
from app.schemas import (
    CharacterResponse, 
    AdminCharacterResponse,
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

@router.get(
    path="/{character_id}",
    description="모든 캐릭터를 조회하는 API입니다.",
    responses={
        200: {"model": AdminCharacterResponse, "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_character(character_id: int, admin_id: AdminUser, chararter_service: CharacterServiceDep) -> AdminCharacterResponse:
    return chararter_service.get_character_by_id(character_id)
