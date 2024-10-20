from fastapi import WebSocket, HTTPException
from sqlalchemy.orm import Session
import json

from ..core import setup_logger, verify_token
from ..models.users import User
from ..models.chats import Chat
from ..utils.socket_room_manager import RoomManager
from ..utils.socket_connection_manager import ConnectionManager
from ..schemas.request.chat_log_request_schema import ChatLogCreate
from ..schemas.chatting_schema import AuthMessage
from ..services import ChatService, UserService, ChatLogService


logger = setup_logger()

async def authenticate_user(websocket: WebSocket, db: Session) -> User:
    """
    WebSocket을 통해 인증 메시지를 수신하고 사용자를 인증하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        db (Session): 데이터베이스 세션 객체.

    Returns:
        User: 인증된 사용자 객체.

    Raises:
        HTTPException: 인증 실패 시 예외 발생.
    """
    try:
        auth_message = await websocket.receive_text()
        auth_data = AuthMessage(**json.loads(auth_message))
        print(auth_data)

        if auth_data.type != "auth" or not auth_data.token:
            raise HTTPException(status_code=1008, detail="Authentication failed: Invalid authentication type or missing token")
        
        user_id = verify_token(auth_data.token)
        user = UserService.get_user_by_id(user_id, db=db)
        return user

    except json.JSONDecodeError:
        raise HTTPException(status_code=1008, detail="Authentication failed: Invalid JSON format")
    except HTTPException as e:
        raise HTTPException(status_code=1008, detail=f"Token validation failed: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=1008, detail=f"Authentication failed: {str(e)}")

async def validate_chat_room(chat_id: int, user: User, db: Session) -> Chat:
    """
    사용자가 특정 채팅 방에 참여할 수 있는지 검증하는 함수

    Args:
        chat_id (int): 채팅 방 ID.
        user (User): 사용자 객체.
        db (Session): 데이터베이스 세션 객체.

    Returns:
        Chat: 채팅 방 객체.

    Raises:
        HTTPException: 사용자가 채팅 방에 참여할 수 없는 경우 예외 발생.
    """
    chat = ChatService.get_chat_by_chat_id_and_user_id(chat_id, user.user_id, db)
    if not chat:
        raise HTTPException(status_code=1008, detail=f"Chat room validation failed: User ({user.user_name}) {user.user_name} is not authorized to join room {chat_id}")
    return chat

async def handle_disconnect(websocket: WebSocket, room_manager: RoomManager, room: ConnectionManager, chat_id: int, user: User):
    """
    WebSocket 연결이 끊어졌을 때 처리하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        room (ConnectionManager): 연결된 클라이언트 관리 객체.
        chat_id (int): 채팅 방 ID.
        user (User): 사용자 객체.
    """
    room.disconnect(websocket)
    logger.info(f"📌 User {user.user_name}({user.user_id}) disconnected from room {chat_id}")
    await room.broadcast_system_message(f"A client disconnected from {chat_id}.")
    room_manager.cleanup_room(chat_id)

async def handle_exception(websocket: WebSocket, exception: Exception):
    """
    예외 발생 시 WebSocket 연결을 종료하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        exception (Exception): 발생한 예외.
    """
    logger.error(f"❌ An error occurred: {exception}")
    await websocket.close(code=1011)  # Internal Server Error



def create_log_message(message_type: str, chat_id: int, user_name: str, contents: str = None, max_length: int = 100) -> str:
    """
    로그 메시지를 생성합니다.

    Args:
        message_type (str): 메시지 타입 (User 또는 Bot).
        chat_log (ChatLogCreate): 채팅 로그 데이터 객체.
        response_message (str): 봇의 응답 메시지 (옵션).
        max_length (int): 메시지의 최대 길이.

    Returns:
        str: 생성된 로그 메시지.
    """
    contents = contents.replace('\n', ' ')
    if len(contents) > max_length:
        contents = contents[:max_length] + "..."
    
    if message_type == "User":
        return f"▶️  User message received: chat_id: {chat_id}, user_name: {user_name}, contents: {contents}"
    
    if message_type == "Bot":
        return f"▶️  Bot response sent: chat_id: {chat_id}, user_name: {user_name}, response_message: \"{contents}\""
    
    return ""


async def insert_message(chat: Chat, role: str, contents: str, db: Session):
    """
    사용자 메시지를 데이터베이스에 저장합니다.

    Args:
        chat_log (ChatLogCreate): 채팅 로그 데이터 객체.
        db (Session): 데이터베이스 세션 객체.
    """
    chat_log= ChatLogCreate(
        chat_id=chat.chat_id,
        user_id=chat.user_id,
        character_id=chat.character_id,
        role=role,
        contents=contents
    )
    ChatLogService.create_chat_log(chat_log, db)
