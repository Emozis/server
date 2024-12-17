from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..models import User
from .base_crud import BaseCRUD


class UserCRUD(BaseCRUD[User]):
    """
    사용자(User) 관련 CRUD 작업을 처리하는 클래스입니다.
    User 모델에 대한 데이터베이스 조작을 담당합니다.
    """

    def __init__(self, db: Session):
        super().__init__(model=User, db=db, id_field='user_id')

    def get_all_users(self) -> list[User]:
        """
        모든 사용자 목록을 조회합니다.
        
        Returns:
            list[User]: 전체 사용자 객체 리스트
        """
        return self.db.query(self.model).all()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자를 조회합니다.
        활성화 상태와 관계없이 해당 이메일을 가진 모든 사용자를 조회합니다.
        
        Args:
            email (str): 조회할 사용자의 이메일
        
        Returns:
            Optional[User]: 조회된 사용자 객체. 존재하지 않을 경우 None 반환
        """
        return self.db.query(self.model).filter(self.model.user_email == email).first()
    
    def get_active_user_by_email(self, user_email: str) -> Optional[User]:
        """
        이메일로 활성화된 사용자를 조회합니다.
        user_is_active가 True인 사용자만 조회합니다.
        
        Args:
            user_email (str): 조회할 사용자의 이메일
        
        Returns:
            Optional[User]: 조회된 활성 사용자 객체. 존재하지 않을 경우 None 반환
        """
        return self.db.query(self.model)\
            .filter(
                self.model.user_email == user_email,
                self.model.user_is_active == True
            ).first()

    def get_admin_user_by_email_and_role(self, user_email: str) -> Optional[User]:
        """
        이메일로 관리자 권한을 가진 활성화된 사용자를 조회합니다.
        user_role이 'admin'이고 user_is_active가 True인 사용자만 조회합니다.
        
        Args:
            user_email (str): 조회할 관리자의 이메일
        
        Returns:
            Optional[User]: 조회된 관리자 사용자 객체. 존재하지 않을 경우 None 반환
        """
        return self.db.query(self.model)\
            .filter(
                self.model.user_email == user_email,
                self.model.user_role == "admin",
                self.model.user_is_active == True
            ).first()
    
    def get_active_user_by_id(self, user_id: int) -> Optional[User]:
        """
        ID로 활성화된 사용자를 조회합니다.
        user_is_active가 True인 사용자만 조회합니다.
        
        Args:
            user_id (int): 조회할 사용자의 ID
        
        Returns:
            Optional[User]: 조회된 활성 사용자 객체. 존재하지 않을 경우 None 반환
        """
        return self.db.query(self.model)\
            .filter(
                self.model.user_id == user_id,
                self.model.user_is_active == True
            ).first()

    def deactivate_user(self, user_id: int) -> bool:
        """
        특정 사용자를 비활성화합니다.
        사용자의 user_is_active를 False로 설정하고 비활성화 시간을 기록합니다.
        
        Args:
            user_id (int): 비활성화할 사용자의 ID
            
        Returns:
            bool: 비활성화 성공 여부
            
        Raises:
            Exception: 비활성화 처리 중 오류가 발생한 경우
        """
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
