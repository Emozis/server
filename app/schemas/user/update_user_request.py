from fastapi_camelcase import CamelModel
from datetime import datetime

from app.models import UserGenderEnum


class UserUpdate(CamelModel):
    # user_email: str | None = None
    user_name: str | None = None
    user_profile: str | None = None
    user_gender: UserGenderEnum | None = None
    user_birthdate: datetime | None = None