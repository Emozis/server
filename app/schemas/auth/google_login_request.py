from fastapi_camelcase import CamelModel


class LoginGoogleIdToken(CamelModel):
    id_token: str