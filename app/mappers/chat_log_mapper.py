from ..models import ChatLog
from ..schemas import ChatLogCreate, ChatLogResponse
from ..schemas.chat.chat_response import CharacterResponse


class ChatLogMapper:
    @staticmethod
    def create_to_model(dto: ChatLogCreate, user_id: int) -> ChatLog:
        return ChatLog(
            chat_id=dto.chat_id,
            user_id=user_id,
            character_id=dto.character_id,
            role=dto.role,
            contents=dto.contents
        )

    @staticmethod
    def to_dto(model: ChatLog) -> ChatLogResponse:
        character_dto = CharacterResponse(
            character_id=model.character.character_id,
            character_name=model.character.character_name,
            character_profile=model.character.character_profile
        ).model_dump()
        return ChatLogResponse(
            log_id=model.log_id,
            character=character_dto,
            role=model.role,
            contents=model.contents,
            log_create_at=model.log_create_at
        )

    @staticmethod
    def to_dto_list(models: list[ChatLog]) -> list[ChatLogResponse]:
        return [ChatLogMapper.to_dto(model) for model in models]