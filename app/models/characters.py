from sqlalchemy import Column, Integer, String, BigInteger, Enum, Text, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database.base import Base
from .enums import CharacterGenderEnum


class Character(Base):
    __tablename__ = "characters"

    character_id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_name = Column(String(255), nullable=False)
    character_profile = Column(String(255), nullable=True)
    character_gender = Column(Enum(CharacterGenderEnum), nullable=True)
    character_personality = Column(String(255), nullable=True)
    character_details = Column(Text, nullable=True)
    character_description = Column(String(255), nullable=True)
    character_greeting = Column(Text, nullable=True)

    character_created_at = Column(TIMESTAMP, server_default=func.now())
    character_updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 

    character_is_public = Column(Boolean, default=True, nullable=False)
    character_likes = Column(Integer, default=0, nullable=False)
    character_usage_count = Column(Integer, default=0, nullable=False)
    character_is_active = Column(Boolean, default=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    user = relationship("User", back_populates="characters")
    chats = relationship("Chat", back_populates="character")
    chat_logs = relationship("ChatLog", back_populates="character")
    character_relationships = relationship("CharacterRelationship", back_populates="character", cascade="all, delete-orphan")