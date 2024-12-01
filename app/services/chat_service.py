from sqlalchemy.orm import Session

from ..core import logger
from ..crud import ChatCRUD, CharacterCRUD
from ..mappers import ChatMapper
from ..schemas import ResponseSchema, ChatCreate, ChatResponse, ChatIdResponse
from ..exceptions import NotFoundException, ForbiddenException


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.chat_crud = ChatCRUD(db)
        self.character_crud = CharacterCRUD(db)

    def create_chat(self, chat: ChatCreate, user_id: int) -> ResponseSchema:
        """
        새로운 채팅방 생성 서비스
        Args:
            chat (ChatCreate): 채팅방 생성에 필요한 데이터
            user_id (int): 채팅방을 생성하는 사용자 ID
        Returns:
            ResponseSchema: 생성된 채팅방 ID를 포함한 응답
        Raises:
            NotFoundException: 캐릭터를 찾을 수 없는 경우
        """
        if not self.character_crud.get_charater_by_id(chat.character_id):
            logger.warning(f"❌ Failed to find character with id {chat.character_id}")
            raise NotFoundException("캐릭터를 찾을 수 없습니다.", "character_id", chat.character_id)
        
        created_chat = self.chat_crud.create(ChatMapper.create_to_model(chat, user_id))
        logger.info(f"✨ Successfully created chat room: {created_chat.chat_id} with character {chat.character_id}")

        return ResponseSchema(
            message="채팅방이 성공적으로 생성되었습니다.",
            data=ChatIdResponse(chat_id=created_chat.chat_id)
            )

    def get_chats_by_user_id(self, user_id: int) -> list[ChatResponse]:
        """
        사용자의 모든 채팅방 조회
        Args:
            user_id (int): 조회할 사용자 ID
        Returns:
            list[ChatResponse]: 마지막 메시지 시간순으로 정렬된 채팅방 목록
        """
        chats = self.chat_crud.get_chats_by_user_id_order_by_last_message_at(user_id)
        logger.info(f"🏠 Found {len(chats)} chat rooms for user {user_id}")
        return ChatMapper.to_dto_list(chats)

    def get_chat_by_chat_id_and_user_id(self, chat_id: int, user_id: int) -> ChatResponse:
        """
        채팅방 ID와 사용자 ID로 특정 채팅방 조회
        Args:
            chat_id (int): 조회할 채팅방 ID
            user_id (int): 조회할 사용자 ID
        Returns:
            ChatResponse: 조회된 채팅방 정보
        Raises:
            NotFoundException: 채팅방을 찾을 수 없는 경우 
        """
        chat = self.chat_crud.get_chat_by_chat_id_and_user_id(chat_id, user_id)
        if not chat:
            logger.warning(f"❌ Failed to find chat with id {chat_id} for user {user_id}")
            raise NotFoundException("채팅방을 찾을 수 없습니다.", "chat_id", chat_id)
        
        logger.info(f"🏠 Successfully retrieved chat: room {chat_id} for user {user_id}")
        return ChatMapper.to_dto(chat)

    def delete_chat(self, chat_id: int, user_id: int) -> ResponseSchema:
        """
        채팅방 삭제
        Args:
            chat_id (int): 삭제할 채팅방 ID
            user_id (int): 요청하는 사용자 ID
        Returns:
            ResponseSchema: 삭제된 채팅방 ID를 포함한 응답
        Raises:
            NotFoundException: 채팅방을 찾을 수 없는 경우
            ForbiddenException: 권한이 없는 경우
        """
        chat = self.chat_crud.get_by_id(chat_id)
        if not chat:
            logger.warning(f"❌ Failed to find chat with id {chat_id}")
            raise NotFoundException("채팅방을 찾을 수 없습니다.", "chat_id", chat_id)
        
        if user_id != chat.user_id:
            logger.warning(f"❌ User {user_id} attempted to modify chat {chat_id} owned by user {chat.user_id}")
            raise ForbiddenException("자신의 채팅방만 삭제할 수 있습니다.", "chat_id", chat_id)
        
        if self.chat_crud.delete(chat_id):
            logger.info(f"🗑️  Successfully deleted chat: room{chat_id} (ID: {chat_id})")
            return ResponseSchema(
                message="채팅방이 성공적으로 삭제되었습니다.",
                data=ChatIdResponse(chat_id=chat_id)
                )