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
        """
        새로운 관계 생성 서비스
        Args:
            relationship (RelationshipCreate): 관계 생성에 필요한 데이터
        Returns:
            MessageResponse: 생성 성공 메세지
        """
        created = self.relationship_crud.create(RelationshipMapper.create_to_model(relationship))
        logger.info(f"✅ Successfully created relationship: {created.relationship_name} (ID: {created.relationship_id})")
        return MessageResponse(message="관계가 성공적으로 생성되었습니다.")

    def get_relationships(self) -> list[RelationshipResponse]:
        """
        모든 관계 조회
        Returns:
            list[RelationshipResponse]: 조회된 모든 관계 정보 리스트
        """
        relationships = self.relationship_crud.get_all()
        logger.info(f"🤝 Total {len(relationships)} relationships found")
        return RelationshipMapper.to_dto_list(relationships)
    
    def get_relationship_by_id(self, relationship_id: int) -> RelationshipResponse:
        """
        ID로 관계 조회
        Args:
            relationship_id (int): 조회할 관계 ID
        Returns:
            RelationshipResponse: 조회된 관계 정보
        Raises:
            NotFoundException: 관계를 찾을 수 없는 경우
        """
        db_relationship = self.relationship_crud.get_by_id(relationship_id)
        if not db_relationship:
            logger.warning(f"❌ Failed to find relationship with id {relationship_id}")
            raise NotFoundException("관계를 찾을 수 없습니다.", "relationship_id", relationship_id)

        logger.info(f"🤝 Found relationship: {db_relationship.relationship_name} (ID: {relationship_id})")
        return RelationshipMapper.to_dto(self.relationship_crud.get_by_id(relationship_id))

    def update_relationship(self, relationship_id: int, relationship_data: RelationshipUpdate) -> RelationshipResponse:
        """
        관계 정보 업데이트
        Args:
            relationship_id (int): 업데이트할 관계 ID
            relationship_data (RelationshipUpdate): 업데이트할 관계 정보
        Returns:
            RelationshipResponse: 업데이트된 관계 정보
        Raises:
            NotFoundException: 관계를 찾을 수 없는 경우
        """
        self.get_relationship_by_id(relationship_id)
        updated = self.relationship_crud.update(relationship_id, RelationshipMapper.update_to_model(relationship_data))

        logger.info(f"✅ Successfully updated relationship: {updated.relationship_name} (ID: {relationship_id})")
        return MessageResponse(message="관계가 성공적으로 수정되었습니다.")

    def delete_relationship(self, relationship_id: int) -> MessageResponse:
        """
        관계 삭제
        Args:
            relationship_id (int): 삭제할 관계 ID
        Returns:
            MessageResponse: 삭제 성공 메세지
        Raises:
            NotFoundException: 관계를 찾을 수 없는 경우
        """
        relationship = self.get_relationship_by_id(relationship_id)
        if self.relationship_crud.delete(relationship_id):
            logger.info(f"✅ Successfully deleted relationship: {relationship.relationship_name} (ID: {relationship_id})")
            return MessageResponse(message="관계가 성공적으로 삭제되었습니다.")