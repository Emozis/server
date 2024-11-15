from fastapi_camelcase import CamelModel


class User(CamelModel):
    user_id: int
    user_email: str
    user_name: str
    user_profile: str | None = None

class LoginResponse(CamelModel):
    status: str
    message: str
    user: User
    access_token: str