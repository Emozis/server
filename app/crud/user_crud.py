from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

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
    
    def get_active_user_by_email(self, user_email: str) -> Optional[User]:
        """활성화된 유저를 user_email로 조회"""
        return self.db.query(self.model)\
            .filter(
                self.model.user_email == user_email,
                self.model.user_is_active == True
            ).first()
    
    def get_active_user_by_id(self, user_id: int) -> Optional[User]:
        """활성화된 유저를 user_id로 조회"""
        return self.db.query(self.model)\
            .filter(
                self.model.user_id == user_id,
                self.model.user_is_active == True
            ).first()

    def deactivate_user(self, user_id: int) -> bool:
        """유저 비활성화 (soft delete)"""
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False

            user.user_is_active = False
            user.user_deactived_at = datetime.now()
            self.db.commit()
            self.db.refresh(user)
            return True

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to deactivate user: {str(e)}")
