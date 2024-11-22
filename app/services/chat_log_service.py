from sqlalchemy.orm import Session

from ..core import logger
from ..crud import ChatLogCRUD
from ..mappers import ChatLogMapper
from ..schemas import ResponseSchema, ChatLogCreate, ChatLogResponse
from ..exceptions import NotFoundException, ForbiddenException


class ChatLogService:
    def __init__(self, db: Session):
        self.db = db
        self.chat_log_crud = ChatLogCRUD(db)

    def create_chat_log(self, chat_log: ChatLogCreate, user_id: int) -> ResponseSchema:
        """
        새로운 채팅 로그 생성 서비스
        Args:
            chat_log (ChatLogCreate): 채팅 로그 생성에 필요한 데이터
            user_id (int): 채팅 로그를 생성하는 사용자 ID
        Returns:
            ResponseSchema: 생성된 채팅 로그 ID를 포함한 응답
        """
        chat_log = self.chat_log_crud.create(ChatLogMapper(chat_log, user_id))
        logger.info(f"✨ Successfully created chat log: {chat_log.log_id} by user {user_id}")
        return ResponseSchema(
            message="채팅 로그가 성공적으로 생성되었습니다.",
            data={"chat_id" : chat_log.log_id}
        )

    def get_chat_logs_by_chat_id(self, chat_id: int, user_id: int) -> list[ChatLogResponse]:
        """
        특정 채팅방의 모든 채팅 로그 조회
        Args:
            chat_id (int): 조회할 채팅방 ID
            user_id (int): 조회하는 사용자 ID
        Returns:
            list[ChatLogResponse]: 채팅 로그 목록
        """
        chat_logs = self.chat_log_crud.get_chat_logs_by_chat_id_and_user_id(chat_id, user_id)
        logger.info(f"📜 Found {len(chat_logs)} chat logs for chat {chat_id} and user {user_id}")
        return ChatLogMapper.to_dto_list(chat_logs)

    def delete_chat(self, log_id: int, user_id: int) -> ResponseSchema:
        """
        채팅 로그 삭제
        Args:
            log_id (int): 삭제할 채팅 로그 ID
            user_id (int): 요청하는 사용자 ID
        Returns:
            ResponseSchema: 삭제된 채팅 로그 ID를 포함한 응답
        Raises:
            NotFoundException: 채팅 로그를 찾을 수 없는 경우
            ForbiddenException: 권한이 없는 경우
        """
        log = self.chat_log_crud.get_by_id(log_id)
        if not log:
            logger.warning(f"❌ Failed to find chat log with id {log_id}")
            raise NotFoundException("채팅 로그를 찾을 수 없습니다.", "log_id", log_id)
        
        if user_id != log.user_id:
            logger.warning(f"❌ User {user_id} attempted to modify chat log {log_id} owned by user {log.user_id}")
            raise ForbiddenException("자신의 채팅 로그만 삭제할 수 있습니다.")

        if self.chat_log_crud.delete(log_id):
            logger.info(f"🗑️  Successfully deleted chat log: log{log_id} (ID: {log_id})")
            return ResponseSchema(
                message="채팅 로그가 성공적으로 삭제되었습니다.",
                data={"log_id" : log_id}
            )