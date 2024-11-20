from sqlalchemy.orm import Session, joinedload

from ..models import Character, CharacterRelationship
from .base_crud import BaseCRUD


class CharacterCRUD(BaseCRUD[Character]):
    def __init__(self, db: Session):
        super().__init__(model=Character, db=db, id_field='character_id')

    def get_charaters(self):
        return self.db.query(Character).options(joinedload(Character.user), joinedload(Character.character_relationships).joinedload(CharacterRelationship.relationship)).all()

    def get_charater(self, character_id: int):
        return self.db.query(Character).options(joinedload(Character.user), joinedload(Character.character_relationships).joinedload(CharacterRelationship.relationship)).filter(Character.character_id == character_id).first()