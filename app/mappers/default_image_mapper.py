from ..models import DefaultImages
from ..schemas import DefaultImageCreate, DefaultImageUpdate, DefaultImageResponse

class DefaultImageMapper:
    @staticmethod
    def create_to_model(dto: DefaultImageCreate) -> DefaultImages:
        return DefaultImages(
            image_name=dto.image_name,
            image_url=dto.image_url,
            image_gender=dto.image_gender,
            image_age_group=dto.image_age_group,
            image_emotion=dto.image_emotion
        )

    @staticmethod
    def update_to_model(dto: DefaultImageUpdate) -> DefaultImages:
        return DefaultImages(
            image_name=dto.image_name,
            image_url=dto.image_url,
            image_gender=dto.image_gender,
            image_age_group=dto.image_age_group,
            image_emotion=dto.image_emotion
        )
    
    @staticmethod
    def to_dto(model: DefaultImages) -> DefaultImageResponse:
        return DefaultImageResponse(
            image_id=model.image_id,
            image_name=model.image_name,
            image_url=model.image_url,
            image_gender=model.image_gender,
            image_age_group=model.image_age_group,
            image_emotion=model.image_emotion,
            image_created_at=model.image_created_at,
            image_updated_at=model.image_updated_at
        )
    
    @staticmethod
    def to_dto_list(models: list[DefaultImages]) -> list[DefaultImageResponse]:
        return [DefaultImageMapper.to_dto(model) for model in models]