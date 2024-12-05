from fastapi import APIRouter, WebSocket

from app.core.dependencies import ChattingServiceDep, RoomManagerDep

router = APIRouter(
    prefix="/api/v1/chatting",
    tags=["Chatting"]
)

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, chatting_service: ChattingServiceDep, room_manager: RoomManagerDep):
    await chatting_service.chatting(websocket, chat_id, room_manager)