from fastapi_camelcase import CamelModel
from pydantic import EmailStr, Field


class LoginRequest(CamelModel):
    user_email: EmailStr = Field(json_schema_extra={"example": "admin@example.com"})
    user_password: str = Field(json_schema_extra={"example": "1234"})