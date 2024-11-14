from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core import logger
from app.crud.user_crud import UserCRUD
from app.models import User


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_crud = UserCRUD(db)

    def create_user(self) -> User:
        """
        새로운 유저 생성 서비스
        Args:
            user_data (dict): 유저 생성에 필요한 데이터
        """
        try:
            # User 모델 인스턴스 생성
            user = User(
                user_email='user_email',
                user_password='user_password',  # 실제로는 해시 처리 필요
                user_name='user_name',
                user_profile='user_profile',
                user_gender='other',
                user_birthdate='2024-01-01'
            )
            
            return self.user_crud.create(user)
            
        except Exception as e:
            logger.error(f"❌ Failed to create user: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to create user: {str(e)}"
            )