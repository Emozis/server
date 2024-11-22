from fastapi import WebSocket, HTTPException
from sqlalchemy.orm import Session
import json

from ..core import logger
from ..services import UserService, ChatService
from ..utils.socket_room_manager import RoomManager
from ..utils import JwtUtil


class ChattingService:
    def __init__(self, db: Session):
        self.room_manager = RoomManager()
        self.user_service = UserService(db)
        self.chat_service = ChatService(db)

    async def chatting(self, websocket: WebSocket, chat_id: int):
        room = self.room_manager.get_room(chat_id)
        await room.connect(websocket)

        try:
            auth_message = await websocket.receive_text()
            auth_data = json.loads(auth_message)
            if auth_data["type"] != "auth" or not auth_data["token"]:
                raise HTTPException(status_code=1008, detail="Authentication failed: Invalid authentication type or missing token")
            
            user_id = await JwtUtil.verify_token(auth_data["token"])

            chat = self.chat_service.get_chat_by_chat_id_and_user_id(chat_id, user_id)
            if not chat:
                raise HTTPException(status_code=1008, detail=f"Chat room validation failed: User (ID: {user_id}) is not authorized to join room {chat_id}")
            
            logger.info(f"🚀 Chatting Start: User {user_id} joined the room {chat_id}")

        except json.JSONDecodeError as e:
            raise HTTPException(status_code=1008, detail="Authentication failed: Invalid JSON format")

            