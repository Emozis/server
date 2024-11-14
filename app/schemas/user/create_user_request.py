from fastapi_camelcase import CamelModel


class UserCreate(CamelModel):
    user_id: int | None = None
    user_email: str
    user_name: str
    user_password: str | None = None
    user_profile: str | None = None
    user_is_active: bool = True