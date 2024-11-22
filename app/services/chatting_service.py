from fastapi import WebSocket, HTTPException
from sqlalchemy.orm import Session
import json
import asyncio

from ..core import logger
from ..services import UserService, ChatService
from ..utils.socket_room_manager import RoomManager
from ..utils import JwtUtil


class ChattingService:
    def __init__(self, db: Session):
        self.room_manager = RoomManager()
        self.user_service = UserService(db)
        self.chat_service = ChatService(db)
        self.AUTH_TIMEOUT = 5

    async def _authenticate_user(self, websocket: WebSocket) -> tuple[int, str, str]:
        """사용자 인증 처리"""
        auth_message = await websocket.receive_text()

        try:
            data_type, data_token = json.loads(auth_message)["type"], json.loads(auth_message)["token"]
        except json.JSONDecodeError:
            raise HTTPException(status_code=1008, detail="Authentication failed: Invalid JSON format")
        
        if data_type != "auth" or not data_token:
            raise HTTPException(status_code=1008, detail=f"Invalid authentication type or missing token - type: {data_type}, token: {data_token[:20]}...")
        
        return await JwtUtil.verify_token(data_token)
    
    async def _validate_chat_access(self, chat_id: int, user_id: int):
        """채팅방 접근 권한 검증"""
        chat = self.chat_service.get_chat_by_chat_id_and_user_id(chat_id, user_id)
        if not chat:
            raise HTTPException(
                status_code=1008, 
                detail=f"User (ID: {user_id}) is not authorized to join room {chat_id}"
            )
        return chat

    async def chatting(self, websocket: WebSocket, chat_id: int):
        room = self.room_manager.get_room(chat_id)
        await room.connect(websocket)

        try:
            # 타임아웃과 함께 인증 수행
            try:
                user_id, user_name, role = await asyncio.wait_for(
                    self._authenticate_user(websocket),
                    timeout=self.AUTH_TIMEOUT
                )
            except asyncio.TimeoutError:
                raise HTTPException(status_code=1008, detail=f"Authentication timeout for room {chat_id}")
            
            # 채팅방 접근 권한 확인
            await self._validate_chat_access(chat_id, user_id)
            
            # 채팅 세션 시작
            logger.info(f"🚀 Chatting Start: User {user_name}({user_id}) joined the room {chat_id}")

        except HTTPException as e:
            await websocket.close(code=e.status_code, reason=e.detail)
            logger.error(f"❌ WebSocket error: {e.detail}")
        except Exception as e:
            await websocket.close(code=1008, reason="Internal server error")
            logger.error(f"❌ Unexpected error: {str(e)}")
        finally:
            await room.disconnect(websocket)