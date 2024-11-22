from fastapi_camelcase import CamelModel
from datetime import datetime


class UserResponse(CamelModel):
    user_id: int
    user_name: str
    user_profile: str

class CharacterResponse(CamelModel):
    character_id: int
    character_name: str
    character_profile: str

class ChatResponse(CamelModel):
    chat_id: int

    user: UserResponse
    character: CharacterResponse

    chat_create_at: datetime
    last_message_at: datetime

    # chat_logs: list[ChatLogs]