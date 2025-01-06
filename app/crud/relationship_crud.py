from sqlalchemy.orm import Session
from typing import Optional

from ..models import Relationship
from .base_crud import BaseCRUD


class RelationshipCRUD(BaseCRUD[Relationship]):
    """
    관계(Relationship) 관련 CRUD 작업을 처리하는 클래스입니다.
    Relationship 모델에 대한 데이터베이스 조작을 담당합니다.
    """

    def __init__(self, db: Session):
        super().__init__(model=Relationship, db=db, id_field='relationship_id')

    def get_user_by_name(self, relationship_name: str) -> Optional[Relationship]:
        """
        관계 이름으로 관계 정보를 조회합니다.
        
        Args:
            relationship_name (str): 조회할 관계의 이름
            
        Returns:
            Optional[Relationship]: 조회된 관계 객체. 존재하지 않을 경우 None 반환
        """
        return self.db.query(self.model).filter(self.model.relationship_name == relationship_name).first()

    def get_relationships_by_ids(self, relationship_ids: list[int]) -> list[Relationship]:
        """
        여러 관계 ID로 관계 정보들을 조회합니다.
        
        Args:
            relationship_ids (List[int]): 조회할 관계 ID 목록
            
        Returns:
            List[Relationship]: 조회된 관계 객체들의 리스트
        """
        if not relationship_ids:
            return []
            
        return self.db.query(self.model)\
            .filter(self.model.relationship_id.in_(relationship_ids))\
            .all()