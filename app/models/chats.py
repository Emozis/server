from sqlalchemy import Column, BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database.base import Base


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    character_id = Column(BigInteger, ForeignKey('characters.character_id'), nullable=False)

    chat_create_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    last_message_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="chats", lazy='selectin')
    character = relationship("Character", back_populates="chats", lazy='selectin')
    chat_logs = relationship("ChatLog", back_populates="chat", lazy='selectin', cascade="all, delete-orphan")