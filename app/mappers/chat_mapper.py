from ..models import Chat
from ..schemas import ChatCreate, ChatResponse
from ..schemas.chat.chat_response import UserResponse, CharacterResponse


class ChatMapper:
    @staticmethod
    def create_to_model(dto: ChatCreate, user_id: int) -> Chat:
        return Chat(
            user_id=user_id,
            character_id=dto.character_id
        )

    @staticmethod
    def to_dto(model: Chat) -> ChatResponse:
        user_dto = UserResponse(
            user_id=model.user.user_id,
            user_name=model.user.user_name,
            user_profile=model.user.user_profile
        )
        character_dto = CharacterResponse(
            character_id=model.character.character_id,
            character_name=model.character.character_name,
            character_profile=model.character.character_profile
        )
        return ChatResponse(
            chat_id=model.chat_id,
            user=user_dto,
            character=character_dto,
            chat_create_at=model.chat_create_at,
            last_message_at=model.last_message_at
        )

    @staticmethod
    def to_dto_list(models: list[Chat]) -> list[ChatResponse]:
        return [ChatMapper.to_dto(model) for model in models]