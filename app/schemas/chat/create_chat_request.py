from fastapi_camelcase import CamelModel


class ChatCreate(CamelModel):
    character_id: int