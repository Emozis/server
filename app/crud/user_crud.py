from sqlalchemy.orm import Session
from typing import Optional, List

from ..models import User
from .base_crud import BaseCRUD


class UserCRUD(BaseCRUD[User]):
    def __init__(self, db: Session):
        """
        UserCRUD 초기화
        Args:
            db: 데이터베이스 세션
        """
        super().__init__(model=User, db=db, id_field='user_id')

    def get_user_by_email(self, email: str) -> Optional[User]:
        """이메일로 유저 조회"""
        return self.db.query(self.model).filter(self.model.user_email == email).first()

    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """활성 상태인 유저만 조회"""
        return self.db.query(self.model).filter(
            self.model.user_is_active == True
        ).offset(skip).limit(limit).all()

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """유저 비활성화 (soft delete)"""
        try:
            user = self.get_by_id(user_id)
            if not user:
                return None

            user.user_is_active = False
            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to deactivate user: {str(e)}")
