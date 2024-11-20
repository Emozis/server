from sqlalchemy.orm import Session

from ..models import CharacterRelationship
from .base_crud import BaseCRUD


class CharacterRelationshipCRUD(BaseCRUD[CharacterRelationship]):
    def __init__(self, db: Session):
        super().__init__(model=CharacterRelationship, db=db, id_field='character_relationship_id')
