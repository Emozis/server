from .auth_service import AuthService
from .user_service import UserService
from .relationship_service import RelationshipService
from .default_image_service import DefaultImageService
from .character_service import CharacterService
from .chat_service import ChatService
from .chat_log_service import ChatLogService
from .chatting_service import ChattingService
from .chatting_session_service import ChattingSessionService


from fastapi import Depends
from sqlalchemy.orm import Session

from ..database.database_manager import get_db

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_relationship_service(db: Session = Depends(get_db)) -> RelationshipService:
    return RelationshipService(db)

def get_default_image_service(db: Session = Depends(get_db)) -> DefaultImageService:
    return DefaultImageService(db)

def get_character_service(db: Session = Depends(get_db)) -> CharacterService:
    return CharacterService(db)

def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    return ChatService(db)

def get_chat_log_service(db: Session = Depends(get_db)) -> ChatLogService:
    return ChatLogService(db)

def get_chatting_service(db: Session = Depends(get_db)) -> ChattingService:
    return ChattingService(db)