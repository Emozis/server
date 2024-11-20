from ..models import Character
from ..schemas import CharacterCreate, CharacterUpdate, CharacterResponse
from ..schemas.character.character_response import CharacterResponse, RelationshipResponse, UserResponse


class CharacterMapper:
    @staticmethod
    def create_to_model(dto: CharacterCreate, user_id: int) -> Character:
        return Character(
            character_name=dto.character_name,
            character_profile=dto.character_profile,
            character_gender=dto.character_gender,
            character_personality=dto.character_personality,
            character_details=dto.character_details,
            character_description=dto.character_description,
            character_greeting=dto.character_greeting,
            character_is_public=dto.character_is_public,
            user_id=user_id
        )

    @staticmethod
    def update_to_model(dto: CharacterUpdate, user_id: int) -> Character:
        return Character(
            character_name=dto.character_name,
            character_profile=dto.character_profile,
            character_gender=dto.character_gender,
            character_personality=dto.character_personality,
            character_details=dto.character_details,
            character_description=dto.character_description,
            character_greeting=dto.character_greeting,
            character_is_public=dto.character_is_public,
            user_id=user_id
        )
    
    @staticmethod
    def to_dto(model: Character) -> CharacterResponse:
        
        relations_dto = [RelationshipResponse(
            relationship_id=cr.relationship.relationship_id,
            relationship_name=cr.relationship.relationship_name
            ) for cr in model.character_relationships]

        user_dto = UserResponse(
            user_id=model.user.user_id,
            user_email=model.user.user_email,
            user_name=model.user.user_name,
            user_profile=model.user.user_profile
        ) if model.user else None

        return CharacterResponse(
            character_id=model.character_id,
            character_name=model.character_name,
            character_profile=model.character_profile,
            character_gender=model.character_gender,
            character_personality=model.character_personality,
            character_details=model.character_details,
            character_relationships=relations_dto,
            character_created_at=model.character_created_at,
            user=user_dto
        )
    
    @staticmethod
    def to_dto_list(models: list[Character]) -> list[CharacterResponse]:
        return [CharacterMapper.to_dto(model) for model in models]