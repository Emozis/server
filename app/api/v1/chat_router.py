from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import ChatServiceDep, CurrentUser
from app.schemas import (
    ErrorResponse, 
    ChatCreate, 
    ChatResponse, 
    ResponseSchema, 
    ChatIdResponse
)


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"]
)

@router.post(
    path="",
    description="새 채팅방을 생성하는 API입니다.",
    responses={
        200: {"model": ResponseSchema[ChatIdResponse], "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def create_chat(chat: ChatCreate, user_id: CurrentUser, chat_service: ChatServiceDep):
    return chat_service.create_chat(chat, user_id)

@router.get(
    path="/me",
    description="인증된 사용자의 모든 채팅방를 조회하는 API입니다.",
    responses={
        200: {"model": list[ChatResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_chat_by_user_id(user_id: CurrentUser, chat_service: ChatServiceDep):
    return chat_service.get_chats_by_user_id(user_id)

@router.delete(
    path="/{chat_id}",
    description="특정 채팅방을 삭제하는 API입니다.",
    responses={
        200: {"model": ResponseSchema[ChatIdResponse], "description": "Successful Response"},
        403: {"model": ErrorResponse, "description": "Forbidden - Access Denied"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def delete_character(chat_id: int, user_id: CurrentUser, chat_service: ChatServiceDep):
    return chat_service.delete_chat(chat_id, user_id)
