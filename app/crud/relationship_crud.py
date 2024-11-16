from sqlalchemy.orm import Session
from typing import Optional

from ..models import Relationship
from .base_crud import BaseCRUD


class RelationshipCRUD(BaseCRUD[Relationship]):
    def __init__(self, db: Session):
        super().__init__(model=Relationship, db=db, id_field='relationship_id')

    def get_user_by_name(self, relationship_name: str) -> Optional[Relationship]:
        return self.db.query(self.model).filter(self.model.relationship_name == relationship_name).first()
