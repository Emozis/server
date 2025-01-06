from sqlalchemy import Column, Enum, String, Text, ForeignKey, BigInteger, Integer, Numeric, TIMESTAMP
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database.base import Base
from .enums import ChatTypeEnum


class ChatLog(Base):
    __tablename__ = "chat_logs"

    log_id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey('chats.chat_id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=True)
    character_id = Column(BigInteger, ForeignKey('characters.character_id'), nullable=True)
    role = Column(Enum(ChatTypeEnum), nullable=False)
    contents = Column(Text, nullable=True)

    log_create_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    model_name = Column(String(255), nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    token_cost = Column(Numeric(10, 4), nullable=True)

    chat = relationship("Chat", back_populates="chat_logs")
    user = relationship("User", back_populates="chat_logs")
    character = relationship("Character", back_populates="chat_logs")

    def to_dict(self):
        """Convert model instance to dictionary with more control."""
        result = {}
        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            # datetime 등 특수 타입 처리
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            result[c.key] = value
        return result