from typing import Annotated
from fastapi import Depends

from .. import services
from ..utils.socket_room_manager import RoomManager
from .auth_config import get_authenticated_user, get_admin_user
from .context import ApplicationContext


# WebSocket Room Manager Dependencies
room_manager = RoomManager()

def get_room_manager() -> RoomManager:
    return ApplicationContext.get_instance().room_manager

RoomManagerDep = Annotated[RoomManager, Depends(get_room_manager)]

# Authentication Dependencies 
AuthenticatedUser = Annotated[int, Depends(get_authenticated_user)]
AdminUser = Annotated[int, Depends(get_admin_user)]

# Service Dependencies
AuthServiceDep = Annotated[services.AuthService, Depends(services.get_auth_service)]
UserServiceDep = Annotated[services.UserService, Depends(services.get_user_service)]
RelationshipServiceDep = Annotated[services.RelationshipService, Depends(services.get_relationship_service)]
DefaultImageServiceDep = Annotated[services.DefaultImageService, Depends(services.get_default_image_service)]
CharacterServiceDep = Annotated[services.CharacterService, Depends(services.get_character_service)]
ChatServiceDep = Annotated[services.ChatService, Depends(services.get_chat_service)]
ChatLogServiceDep = Annotated[services.ChatLogService, Depends(services.get_chat_log_service)]
ChattingServiceDep = Annotated[services.ChattingService, Depends(services.get_chatting_service)]
FeedbackServiceDep = Annotated[services.FeedbackService, Depends(services.get_feedback_service)]