from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import DefaultImages
from .base_crud import BaseCRUD


class DefaultImageCRUD(BaseCRUD[DefaultImages]):
    def __init__(self, db: Session):
        super().__init__(model=DefaultImages, db=db, id_field='image_id')

    def get_total_count(self) -> int:
        """전체 기본 이미지 개수를 반환합니다."""
        return self.db.query(func.count(DefaultImages.image_id)).scalar()