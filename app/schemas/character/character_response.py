from fastapi_camelcase import CamelModel
from datetime import datetime

from ...models.enums import CharacterGenderEnum
from ..relationship.relationship_response import RelationshipResponse


class UserResponse(CamelModel):
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
    character_relationships: list[RelationshipResponse]
    character_created_at: datetime | None = None
    user: UserResponse
