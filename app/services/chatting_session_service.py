from fastapi import WebSocket
from sqlalchemy.orm import Session
import json
import asyncio

from ..core import logger
from ..services import ChatLogService
from ..models import Chat
from ..schemas import UserMessage, CharacterMessage
from ..utils.socket_connection_manager import ConnectionManager
from ..chatbot import data_converter, Gemini, ChatBot


class ChattingSessionService:
    def __init__(self, db: Session, room: ConnectionManager, chat: Chat):
        self.room = room
        self.chat = chat
        self.chat_log_service = ChatLogService(db)
        self.gemini = None
        
    @classmethod
    async def create(cls, db: Session, room: ConnectionManager, chat: Chat):
        """비동기 팩토리 메서드"""
        service = cls(db, room, chat)
        await service.initialize()
        return service
        
    async def initialize(self):
        """비동기 초기화 로직"""
        user_info, character_info, chat_history = await data_converter(
            self.chat.user, 
            self.chat.character, 
            self.chat.chat_logs
        )
        self.gemini = Gemini(
            user_info=user_info,
            character_info=character_info,
            chat_history=chat_history
        )

        self.chatbot = ChatBot(
            user_info=user_info,
            character_info=character_info,
            chat_history=chat_history
    )
        
    async def generate_bot_response(self, inputs: str):
        response_id = self.room.get_next_response_id()

        output = ""
        # async for char in self.gemini.astream_yield(inputs):
        async for char in self.chatbot.astream(inputs):
            output += char
            await self.send_socket_response(char, response_id)
                # await asyncio.sleep(0.2)

        await self.send_socket_response("[EOS]", response_id, chatType="end")

        return output
    
    async def _send_greetings(self, chat: Chat, user_id: int) -> None:
        """
        채팅 시작 시 채팅 내역이 비어있다면 첫 인사 전송하는 메소드

        Args:
            chat (Chat): 채팅 방 객체
            user_id (int): 채팅하는 유저 id
        Returns:
            None
        """
        if not chat.chat_logs:
            response_id = self.room.get_next_response_id()
            content = chat.character.character_greeting
            await self.send_socket_response(content, response_id, chatType="greeting")
            self.chat_log_service.create_chat_log_for_socket(chat.chat_id, chat.character_id, user_id, "character", content)

    async def send_socket_response(self, content: str, response_id: int, chatType: str = "chat"):
        response = CharacterMessage(
            type="character",
            characterName=self.chat.character.character_name,
            responseId=response_id,
            content=content,
            chatType=chatType,
        ).model_dump_json()
        await self.room.broadcast(response)

    async def handle_session(self, websocket: WebSocket, chat: Chat, user_id: int) -> None:
        """
        메인 채팅 로직

        첫 인사 전송 후 사용자의 입력까지 대기 후 답변 생성

        Args:
            websocket (WebSocket): 연결된 웹소켓 객체
            chat (Chat): 채팅이 이루어지는 채팅방 객체
            user_id (int): 채팅 중인 유저 id
        Returns:
            None
        """
        # 첫 채팅일 시 첫인사 전송
        await self._send_greetings(chat, user_id)

        while True:
            # 사용자 메세지 입력
            data = await websocket.receive_text()
            user_message = UserMessage(**json.loads(data))

            # 사용자 메세지 저장
            self.chat_log_service.create_chat_log_for_socket(chat.chat_id, chat.character_id, user_id, "user", user_message.content)

            # 챗봇 답변 생성
            output = await self.generate_bot_response(user_message.content)

            self.gemini.add_history(user_message.content, output)
            self.chat_log_service.create_chat_log_for_socket(chat.chat_id, chat.character_id, user_id, "character", output)

            logger.info(
                f"💬 Chat exchanged in room {chat.chat_id}:\n"
                f"- User: {user_message.content[:30]}{'...' if len(user_message.content) > 30 else ''}\n"
                f"- {chat.character.character_name}: {output[:30]}{'...' if len(output) > 30 else ''}"
            )