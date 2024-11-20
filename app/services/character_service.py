from sqlalchemy.orm import Session

from ..core import logger
from ..models import CharacterRelationship
from ..crud import CharacterCRUD, CharacterRelationshipCRUD, RelationshipCRUD
from ..mappers import CharacterMapper
from ..schemas import CharacterCreate, CharacterUpdate, MessageResponse
from ..exceptions import NotFoundException


class CharacterService:
    def __init__(self, db: Session):
        self.db = db
        self.character_crud = CharacterCRUD(db)
        self.relationship_crud = RelationshipCRUD(db)
        self.character_relationship_crud = CharacterRelationshipCRUD(db)

    def create_character(self, character: CharacterCreate, user_id: int):
        db_charater = self.character_crud.create(CharacterMapper.create_to_model(character, user_id))

        for relationship_id in character.relationships:
            self.character_relationship_crud.create(CharacterRelationship(character_id=db_charater.character_id, relationship_id=relationship_id))
        
        return MessageResponse(message="캐릭터가 성공적으로 생성되었습니다.")
    
    def get_characters(self):
        charaters = self.character_crud.get_charaters()
        return CharacterMapper.to_dto_list(charaters)
    
    def get_character(self, character_id: int):
        charater = self.character_crud.get_charater(character_id)
        if not charater:
            logger.warning(f"❌ Failed to find character with id {character_id}")
        return CharacterMapper.to_dto(charater)

    def update_character(self):
        return
    
    def delete_charactor(self):
        return
