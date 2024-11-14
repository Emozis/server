from sqlalchemy import Boolean, Column, String, DateTime, Enum, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database.base import Base
from .enums import UserGenderEnum


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_email = Column(String(255), unique=True, nullable=True)
    user_password = Column(String(255))
    user_name = Column(String(255))
    user_profile = Column(String(255))
    user_join_date = Column(DateTime, default=datetime.now)
    user_is_active = Column(Boolean, default=True)

    user_gender = Column(Enum(UserGenderEnum), nullable=True)
    user_birthdate = Column(DateTime, nullable=True)

    chats = relationship("Chat", back_populates="user")
    chat_logs = relationship("ChatLog", back_populates="user")
    characters = relationship("Character", back_populates="user")