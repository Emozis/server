from fastapi_camelcase import CamelModel

from ...models.enums import CharacterGenderEnum


class Relationship(CamelModel):
    relationship_id: int
    relationship_name: str | None = None

class CharacterCreate(CamelModel):
    character_name: str
    character_profile: str
    character_gender: CharacterGenderEnum
    character_personality: str
    character_details: str
    character_description: str
    character_greeting: str
    character_is_public: bool
    character_relationships: list[Relationship]