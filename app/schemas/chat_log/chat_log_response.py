from fastapi_camelcase import CamelModel
from datetime import datetime
from enum import Enum


class CharacterResponse(CamelModel):
    character_id: int
    character_name: str
    character_profile: str

class ChatLogRoolEnum(str, Enum):
    user = 'user'
    character = 'character'

class ChatLogResponse(CamelModel):
    log_id: int
    character: CharacterResponse
    role: ChatLogRoolEnum
    contents: str
    log_create_at: datetime