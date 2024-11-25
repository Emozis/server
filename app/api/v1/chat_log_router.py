from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import ChatLogServiceDep, CurrentUser
from app.schemas import ResponseSchema, ErrorResponse, ChatLogResponse


router = APIRouter(
    prefix="/api/v1/chat-log",
    tags=["Chat log"]
)

@router.get(
    path="/chats",
    description="특정 채팅방의 채팅 로그를 조회하는 API입니다. 인증된 사용자가 자신의 채팅 로그를 조회할 수 있습니다.",
    responses={
        200: {"model": list[ChatLogResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_chat_logs_by_chat_id(chat_id: int, user_id: CurrentUser, chat_log_service: ChatLogServiceDep) -> list[ChatLogResponse]:
    return chat_log_service.get_chat_logs_by_chat_id(chat_id, user_id)

@router.delete(
    path="/{log_id}",
    description="특정 채팅 로그를 삭제하는 API입니다. 인증된 사용자가 자신의 채팅 로그를 삭제할 수 있습니다.",
    responses={
        200: {"model": ResponseSchema, "description": "Successful Response"},
        403: {"model": ErrorResponse, "description": "Forbidden - Access Denied"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def delete_chat_log(log_id: int, user_id: CurrentUser, chat_log_service: ChatLogServiceDep) -> ResponseSchema:
    return chat_log_service.delete_chat_log(log_id, user_id)