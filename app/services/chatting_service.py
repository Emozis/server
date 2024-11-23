from fastapi import WebSocket, HTTPException, WebSocketDisconnect
from sqlalchemy.orm import Session
import json
import asyncio
import traceback

from ..core import logger
from ..services import UserService, ChatService
from ..crud import ChatCRUD
from ..models import Chat
from ..schemas import AuthMessage, UserMessage
from ..chatbot import data_converter, Gemini
from ..utils import JwtUtil, RoomManager


class ChattingService:
    def __init__(self, db: Session, room_manager: RoomManager):
        self.room_manager = room_manager
        self.user_service = UserService(db)
        self.chat_service = ChatService(db)
        self.chat_crud = ChatCRUD(db)
        self.AUTH_TIMEOUT = 5

    async def _authenticate_user(self, websocket: WebSocket) -> tuple[int, str, str]:
        """사용자 인증 처리"""
        try:
            auth_message = AuthMessage(**json.loads(await websocket.receive_text()))
        except json.JSONDecodeError:
            raise HTTPException(status_code=1008, detail="Authentication failed: Invalid JSON format")
        
        if auth_message.type != "auth" or not auth_message.token:
            raise HTTPException(status_code=1008, detail=f"Invalid authentication type or missing token - type: {auth_message.type}, token: {auth_message.token[:20]}...")
        
        return await JwtUtil.verify_token(auth_message.token)
    
    async def _validate_chat_access(self, chat_id: int, user_id: int) -> Chat:
        """채팅방 접근 권한 검증"""
        chat = self.chat_crud.get_chat_by_chat_id_and_user_id(chat_id, user_id)
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
            chat = await self._validate_chat_access(chat_id, user_id)
            
            # Make Initial Data
            user_info, character_info, chat_history = await data_converter(chat.user, chat.character, chat.chat_logs)

            # Make Gemini Chain
            gemini = Gemini(
                user_info = user_info,
                character_info = character_info, 
                chat_history = chat_history
            )

            # 채팅 세션 시작
            logger.info(f"🚀 Chatting Start: User {user_name}({user_id}) started chatting with {chat.character.character_name}({chat.character.character_id}) in room {chat_id}")
            
            while True:
                data = await websocket.receive_text()
                user_message = UserMessage(**json.loads(data))
                await room.broadcast("dddd")

        except WebSocketDisconnect:
            logger.info(f"👋 WebSocket disconnected normally: User {user_name}({user_id}) left chat room {chat_id} with {chat.character.character_name}({chat.character.character_id})")
        except json.JSONDecodeError:
            await websocket.close(code=1008, reason="Authentication failed: Invalid JSON format")
            logger.error("❌ Authentication failed: Invalid JSON format")
        except HTTPException as e:
            await websocket.close(code=e.status_code, reason=e.detail)
            logger.error(f"❌ WebSocket error: {e.detail}")
        except Exception as e:
            error_detail = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'traceback': traceback.format_exc()
            }
            logger.error(
                f"❌ Unexpected error:\n"
                f"- Error Type: {error_detail['error_type']}\n"
                f"- Error Message: {error_detail['error_message']}\n"
                f"- Traceback:\n{error_detail['traceback']}"
            )
            await websocket.close(code=1008, reason="Internal server error")
        finally:
            await room.disconnect(websocket)