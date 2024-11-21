from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import DefaultImages
from .base_crud import BaseCRUD


class DefaultImageCRUD(BaseCRUD[DefaultImages]):
    """
    기본 이미지 관련 CRUD 작업을 처리하는 클래스입니다.
    DefaultImages 모델에 대한 데이터베이스 조작을 담당합니다.
    """
    
    def __init__(self, db: Session):
        super().__init__(model=DefaultImages, db=db, id_field='image_id')

    def get_total_count(self) -> int:
        """
        저장된 기본 이미지의 총 개수를 반환합니다.
        
        Returns:
            int: 기본 이미지의 총 개수
        """
        return self.db.query(func.count(DefaultImages.image_id)).scalar()