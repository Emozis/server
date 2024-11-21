from sqlalchemy.orm import Session

from ..models import CharacterRelationship
from .base_crud import BaseCRUD


class CharacterRelationshipCRUD(BaseCRUD[CharacterRelationship]):
    """
    캐릭터 관계(CharacterRelationship) 관련 CRUD 작업을 처리하는 클래스입니다.
    CharacterRelationship 모델에 대한 데이터베이스 조작을 담당하며,
    캐릭터 간의 관계 정보를 관리합니다.
    """
    
    def __init__(self, db: Session):
        super().__init__(model=CharacterRelationship, db=db, id_field='character_relationship_id')
