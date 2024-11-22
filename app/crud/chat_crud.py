from sqlalchemy.orm import Session

from ..models import Chat
from .base_crud import BaseCRUD


class ChatCRUD(BaseCRUD[Chat]):
    """
    채팅 관련 CRUD 작업을 처리하는 클래스입니다.
    Chat 모델에 대한 데이터베이스 조작을 담당합니다.
    """

    def __init__(self, db: Session):
        super().__init__(model=Chat, db=db, id_field='chat_id')

    def get_chats_by_user_id_order_by_last_message_at(self, user_id: int):
        """
        특정 사용자의 모든 채팅을 최근 메시지 시간 순으로 조회합니다.
        
        Args:
            user_id (int): 조회할 사용자의 ID
            
        Returns:
            list[Chat]: 해당 사용자의 채팅 목록 (최근 메시지 시간 순으로 정렬됨)
        """
        return self.db.query(Chat)\
            .filter(Chat.user_id == user_id)\
            .order_by(Chat.last_message_at.desc())\
            .all()