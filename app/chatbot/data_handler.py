from ..models import User, Character, ChatLog

async def data_converter(user: User, character: Character, chat_logs: list[ChatLog]) -> tuple[dict[str, object], dict[str, object], list[dict[str, str]]]:

    user_info = {
        "user_name": user.user_name,
        "user_birthdate": user.user_birthdate,
        "user_gender": user.user_gender.value
    }

    character_info = {
        "character_name": character.character_name,
        "character_gender": character.character_gender.value,
        "character_personality": character.character_personality,
        "character_details": character.character_details,
        "relation_type": ", ".join([c.relationship.relationship_name for c in character.character_relationships])
    }

    chat_history = [{"role": log.role.value, "content": log.contents} for log in chat_logs]

    return user_info, character_info, chat_history