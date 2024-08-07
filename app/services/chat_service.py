from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..crud import chat_crud
from ..models import Chat
from ..schemas.request.chat_request_schema import ChatCreate

class ChatService:
    # insert
    @staticmethod
    def create_chat(chat: ChatCreate, db: Session):
        return chat_crud.create_chat(chat, db)

    # select
    @staticmethod
    def get_chats_by_user_id(user_id: int, db: Session) -> list[Chat]:
        chats = chat_crud.get_chats_by_user_id(user_id, db)
        
        for idx in range(len(chats)):
            if len(chats[idx].chat_logs) > 0:
                chats[idx].chat_logs = [chats[idx].chat_logs[-1]]

        return chats

    @staticmethod
    def get_chat_by_chat_id_and_user_id(chat_id: int, user_id: int, db: Session) -> Chat:
        return chat_crud.get_chats_by_chat_id_and_user_id(chat_id, user_id, db)

    # delete
    @staticmethod
    def delete_chat_by_id(chat_id: int, user_id: int, db: Session) -> bool:
        success = chat_crud.delete_chat_by_id(chat_id, user_id, db)
        if not success:
            raise HTTPException(status_code=404, detail="Chat not found or not authorized to delete")
        return success
