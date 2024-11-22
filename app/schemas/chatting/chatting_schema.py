from pydantic import BaseModel


class AuthMessage(BaseModel):
    type: str
    token: str

class UserMessage(BaseModel):
    type: str
    content: str

class SystemMessage(BaseModel):
    type: str
    characterName: str
    responseId: int
    content: str

class CharacterMessage(BaseModel):
    type: str
    characterName: str
    responseId: int
    content: str