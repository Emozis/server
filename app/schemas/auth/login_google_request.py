from fastapi_camelcase import CamelModel


class LoginGoogleRequest(CamelModel):
    id_token: str