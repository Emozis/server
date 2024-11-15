from fastapi_camelcase import CamelModel
from pydantic import EmailStr


class LoginRequest(CamelModel):
    user_email: EmailStr
    user_password: str