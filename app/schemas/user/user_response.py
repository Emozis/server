from fastapi_camelcase import CamelModel
from pydantic import ConfigDict
from datetime import datetime

from app.models import UserGenderEnum


class UserResponse(CamelModel):
    user_id: int
    user_email: str
    user_name: str
    user_profile: str | None = None
    user_gender: UserGenderEnum | None = None
    user_birthdate: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(CamelModel):
    message: str