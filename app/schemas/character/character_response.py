from fastapi_camelcase import CamelModel
from datetime import datetime

from ...models.enums import CharacterGenderEnum


class Relationship(CamelModel):
    relationship_id: int
    relationship_name: str

class CharacterRelationships(CamelModel):
    relationship: Relationship

class User(CamelModel):
    user_id: int
    user_email: str
    user_name: str
    user_profile: str | None = None
    
class CharacterResponse(CamelModel):
    character_id: int
    character_name: str
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    character_relationships: list[CharacterRelationships]
    character_created_at: datetime | None = None
    user: User
