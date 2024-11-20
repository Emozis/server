from sqlalchemy.orm import Session

from ..models import Character
from .base_crud import BaseCRUD


class CharacterCRUD(BaseCRUD[Character]):
    def __init__(self, db: Session):
        super().__init__(model=Character, db=db, id_field='character_id')
