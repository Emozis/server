from fastapi_camelcase import CamelModel
from enum import Enum


class ChatLogRoolEnum(str, Enum):
    user = 'user'
    character = 'character'

class ChatLogCreate(CamelModel):
    chat_id: int
    character_id: int | None = None
    role: ChatLogRoolEnum
    contents: str