from .users import User
from .characters import Character
from .relationships import Relationship
from .character_relationships import CharacterRelationship
from .default_images import DefaultImages

from .chats import Chat
from .chat_logs import ChatLog

from .enums import UserGenderEnum, CharacterGenderEnum, ChatTypeEnum, ImageGenderEnum, ImageAgeGroupEnum


from sqlalchemy import event, text
from sqlalchemy.orm import Mapper
from sqlalchemy.engine import Connection

@event.listens_for(Chat, 'after_insert')
def increment_character_usage_count(
    mapper: Mapper[Chat], 
    connection: Connection, 
    target: Chat
) -> None:
    if target.character_id:
        sql = text("""
            UPDATE characters 
            SET character_usage_count = character_usage_count + 1 
            WHERE character_id = :character_id
        """)
        connection.execute(sql, {"character_id": target.character_id})