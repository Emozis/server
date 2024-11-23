from sqlalchemy.orm import Session

from ..core import logger
from ..services import ChatLogService


class ChattingSessionService:
    def __init__(self, db: Session):
        self.chat_log_service = ChatLogService(db)

    async def chatting_session(self):
        pass

    