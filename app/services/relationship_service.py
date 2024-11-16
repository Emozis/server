from sqlalchemy.orm import Session

from ..core import logger
from ..crud import RelationshipCRUD
from ..mappers import RelationshipMapper
from ..schemas import RelationshipCreate, MessageResponse, RelationshipResponse, RelationshipUpdate
from ..exceptions import NotFoundException


class RelationshipService:
    def __init__(self, db: Session):
        self.db = db
        self.relationship_crud = RelationshipCRUD(db)

    def create_relationship(self, relationship: RelationshipCreate) -> MessageResponse:
        self.relationship_crud.create(RelationshipMapper.create_to_model(relationship))
        return MessageResponse(message="관계가 성공적으로 생성되었습니다.")

    def get_relationships(self) -> list[RelationshipResponse]:
        return RelationshipMapper.to_dto_list(self.relationship_crud.get_all())
    
    def get_relationship_by_id(self, relationship_id: int) -> RelationshipResponse:
        db_relationship = self.relationship_crud.get_by_id(relationship_id)
        if not db_relationship:
            logger.warning(f"❌ Failed to find relationship with id {relationship_id}")
            raise NotFoundException("관계를 찾을 수 없습니다.")

        return RelationshipMapper.to_dto(self.relationship_crud.get_by_id(relationship_id))

    def update_relationship(self, relationship_id: int, relationship_data: RelationshipUpdate) -> RelationshipResponse:
        self.get_relationship_by_id(relationship_id)
        db_relationship = self.relationship_crud.update(relationship_id, RelationshipMapper.update_to_model(relationship_data))
        return RelationshipMapper.to_dto(db_relationship)

    def delete_relationship(self, relationship_id: int) -> MessageResponse:
        self.get_relationship_by_id(relationship_id)
        if self.relationship_crud.delete(relationship_id):
            return MessageResponse(message="관계가 성공적으로 삭제되었습니다.")