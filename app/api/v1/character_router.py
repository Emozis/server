from fastapi import APIRouter
from fastapi import Form, File, UploadFile
from pydantic import ValidationError

from app.core import handle_exceptions
from app.core.dependencies import CharacterServiceDep, CurrentUser
from app.schemas import CharacterCreate, CharacterUpdate, DefaultImageResponse, MessageResponse, ErrorResponse
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
    description="공개된 모든 캐릭터를 조회하는 API입니다.",
)
@handle_exceptions
async def get_public_characters(chararter_service: CharacterServiceDep):
    return chararter_service.get_public_characters()

@router.get(
    path="/rank/",
    description="사용 횟수가 높은 상위 5개의 공개된 캐릭터를 조회하는 API입니다.",
)
@handle_exceptions
async def get_top_used_public_characters(chararter_service: CharacterServiceDep):
    return chararter_service.get_top_used_public_characters(limit=5)

@router.get(
    path="/me/",
    description="인증된 사용자의 모든 캐릭터를 조회하는 API입니다.",
)
@handle_exceptions
async def get_characters_by_user_id(user_id: CurrentUser, chararter_service: CharacterServiceDep):
    return chararter_service.get_characters_by_user_id(user_id)

@router.get(
    path="/{character_id}",
    description="특정 캐릭터를 조회하는 API입니다.",
)
@handle_exceptions
async def get_character_by_id(chararter_id: int, chararter_service: CharacterServiceDep):
    return chararter_service.get_character_by_id(chararter_id)

@router.put(
    path="/{character_id}",
    description="특정 캐릭터 정보를 업데이트하는 API입니다.",
)
@handle_exceptions
async def update_character(character_id: int, character: CharacterUpdate, user_id: CurrentUser, chararter_service: CharacterServiceDep):
    return chararter_service.update_character(character_id, character, user_id)

@router.patch(
    path="/{character_id}/deactive",    
    description="특정 캐릭터를 비활성화하는 API입니다.",
)
async def deactive_character(character_id: int, user_id: CurrentUser, chararter_service: CharacterServiceDep):
    return chararter_service.deactive_charactor(character_id, user_id)

@router.delete(
    path="/{character_id}",
    description="특정 캐릭터를 삭제하는 API입니다.",
)
@handle_exceptions
async def delete_character(character_id: int, user_id: CurrentUser, chararter_service: CharacterServiceDep):
    return chararter_service.delete_charactor(character_id, user_id)
