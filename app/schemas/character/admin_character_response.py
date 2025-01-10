from fastapi_camelcase import CamelModel
from datetime import datetime

from ...models.enums import CharacterGenderEnum
from ..relationship.relationship_response import RelationshipResponse
from .character_response import UserResponse

    
class AdminCharacterResponse(CamelModel):
    character_id: int
    character_name: str
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    character_description: str | None = None
    character_greeting: str | None = None
    character_relationships: list[RelationshipResponse]
    character_created_at: datetime
    character_updated_at: datetime
    character_is_public: bool
    character_likes: int
    character_usage_count: int
    user: UserResponse
