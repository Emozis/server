from fastapi_camelcase import CamelModel
from datetime import datetime


class DefaultImageResponse(CamelModel):
    image_id: int
    image_name: str
    image_url: str
    image_gender: str
    image_age_group: str
    image_emotion: str = None

    image_created_at: datetime | None = None
    image_updated_at: datetime | None = None