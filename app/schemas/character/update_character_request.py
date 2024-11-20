from fastapi_camelcase import CamelModel

from ...models.enums import CharacterGenderEnum


class CharacterUpdate(CamelModel):
    character_name: str
    character_profile: str
    character_gender: CharacterGenderEnum
    character_personality: str
    character_details: str
    character_description: str
    character_greeting: str
    character_is_public: bool
    relationships: list[int] = []