from sqlalchemy.orm import Session

from ..models import ChatLog
from .base_crud import BaseCRUD


class ChatLogCRUD(BaseCRUD[ChatLog]):
    """
    채팅 로그 관련 CRUD 작업을 처리하는 클래스입니다.
    ChatLog 모델에 대한 데이터베이스 조작을 담당합니다.
    """

    def __init__(self, db: Session):
        super().__init__(model=ChatLog, db=db, id_field='log_id')

    def get_chat_logs_by_chat_id_and_user_id(self, chat_id: int, user_id: int) -> list[ChatLog]:
        """
        특정 채팅과 사용자에 해당하는 모든 채팅 로그를 생성 시간순으로 조회합니다.
        
        Args:
            chat_id (int): 조회할 채팅의 ID
            user_id (int): 조회할 사용자의 ID
            
        Returns:
            list[ChatLog]: 해당하는 채팅 로그 목록 (생성 시간순으로 정렬됨)
        """
        return self.db.query(ChatLog)\
            .filter(ChatLog.chat_id == chat_id)\
            .filter(ChatLog.user_id == user_id)\
            .order_by(ChatLog.log_create_at)\
            .all()