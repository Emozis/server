from sqlalchemy.orm import Session

from ..models import ChatLog
from .base_crud import BaseCRUD


class ChatLogCRUD(BaseCRUD[ChatLog]):
    def __init__(self, db: Session):
        super().__init__(model=ChatLog, db=db, id_field='log_id')

    def get_chat_logs_by_chat_id_and_user_id(self, chat_id: int, user_id: int) -> list[ChatLog]:
        return self.db.query(ChatLog)\
            .filter(ChatLog.chat_id == chat_id)\
            .filter(ChatLog.user_id == user_id)\
            .order_by(ChatLog.log_create_at)\
            .all()