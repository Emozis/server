from sqlalchemy import Column, Enum, Text, ForeignKey, BigInteger, Sequence, TIMESTAMP
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

    chat = relationship("Chat", back_populates="chat_logs")
    user = relationship("User", back_populates="chat_logs")
    character = relationship("Character", back_populates="chat_logs")