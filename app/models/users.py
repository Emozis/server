from sqlalchemy import Boolean, Column, String, TIMESTAMP, Enum, BigInteger, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database.base import Base
from .enums import UserGenderEnum, UserRoleEnum


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_email = Column(String(255), unique=True, nullable=True)
    user_password = Column(String(255))
    user_name = Column(String(255))
    user_profile = Column(String(255))
    user_created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_is_active = Column(Boolean, default=True)
    user_deactived_at = Column(TIMESTAMP(timezone=True))

    user_gender = Column(Enum(UserGenderEnum), nullable=True)
    user_role = Column(Enum(UserRoleEnum), nullable=False, default="user")
    user_birthdate = Column(Date, nullable=True)

    chats = relationship("Chat", back_populates="user")
    chat_logs = relationship("ChatLog", back_populates="user")
    characters = relationship("Character", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")