from typing import Generic, TypeVar, Optional
from fastapi_camelcase import CamelModel


T = TypeVar('T')

class ResponseSchema(CamelModel, Generic[T]):
    message: str
    data: Optional[T]

class UserIdResponse(CamelModel):
    user_id: int
    user_name: str

class CharacterIdResponse(CamelModel):
    character_id: int

class ChatIdResponse(CamelModel):
    chat_id: int

class ChatLogIdResponse(CamelModel):
    log_id: int

class DefaultImageIdResponse(CamelModel):
    image_id: int

class RelationshipIdResponse(CamelModel):
    relationship_id: int