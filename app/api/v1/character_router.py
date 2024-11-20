from fastapi import APIRouter
from fastapi import Form, File, UploadFile
from pydantic import ValidationError

from app.core import handle_exceptions
from app.core.dependencies import CharacterServiceDep, CurrentUser
from app.schemas import CharacterCreate, DefaultImageResponse, MessageResponse, ErrorResponse
from app.exceptions.default_image_exception import (
    UnsupportedImageFormatException,
    InvalidEnumValueException
)


router = APIRouter(
    prefix="/api/v1/character",
    tags=["Characters"]
)

@router.post(
    path="/",
    description="새 캐릭터를 생성하는 API입니다.",
)
@handle_exceptions
async def create_character(charater: CharacterCreate, user_id: CurrentUser, chararter_service: CharacterServiceDep):  
    return chararter_service.create_character(charater, user_id)

@router.get(
    path="/",
    description="모든 캐릭터를 조회하는 API입니다.",
)
@handle_exceptions
async def get_characters(chararter_service: CharacterServiceDep):
    return chararter_service.get_characters()

@router.get(
    path="/{character_id}",
    description="특정 캐릭터를 조회하는 API입니다.",
)
@handle_exceptions
async def get_character(chararter_id: int, chararter_service: CharacterServiceDep):
    return chararter_service.get_character(chararter_id)

@router.put(
    path="/{character_id}",
    description="특정 캐릭터 정보를 업데이트하는 API입니다.",
)
@handle_exceptions
async def update_character(chararter_service: CharacterServiceDep):
    return

@router.delete(
    path="/{character_id}",
    description="특정 캐릭터를 삭제하는 API입니다.",
)
@handle_exceptions
async def delete_character(chararter_service: CharacterServiceDep):
    return 
