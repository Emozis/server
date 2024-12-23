from fastapi_camelcase import CamelModel
from pydantic import EmailStr, Field


class LoginRequest(CamelModel):
    user_email: EmailStr = Field(example="admin@example.com")
    user_password: str = Field(example="1234")