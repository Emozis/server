from ..models import Character
from ..schemas import CharacterCreate, CharacterUpdate

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
    
    # @staticmethod
    # def to_dto(model: DefaultImages) -> DefaultImageResponse:
    #     return DefaultImageResponse(
    #         image_id=model.image_id,
    #         image_name=model.image_name,
    #         image_url=model.image_url,
    #         image_gender=model.image_gender,
    #         image_age_group=model.image_age_group,
    #         image_emotion=model.image_emotion,
    #         image_created_at=model.image_created_at,
    #         image_updated_at=model.image_updated_at
    #     )
    
    # @staticmethod
    # def to_dto_list(models: list[DefaultImages]) -> list[DefaultImageResponse]:
    #     return [DefaultImageMapper.to_dto(model) for model in models]