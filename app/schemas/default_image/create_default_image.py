from fastapi_camelcase import CamelModel

from ...models.enums import ImageGenderEnum, ImageAgeGroupEnum, ImageEmotionEnum


class DefaultImageCreate(CamelModel):
    image_name: str = ""
    image_url: str = ""
    image_gender: ImageGenderEnum
    image_age_group: ImageAgeGroupEnum
    image_emotion: ImageEmotionEnum