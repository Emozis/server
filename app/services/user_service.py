from sqlalchemy.orm import Session

from ..core import logger
from ..models import User
from ..crud import UserCRUD
from ..mappers import UserMapper
from ..schemas import UserCreate, UserUpdate, UserResponse, MessageResponse
from ..utils import password_hasher
from ..exceptions import (
    UserNotFoundException,
    UserConflictException
)


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_crud = UserCRUD(db)

    def create_user(self, user: UserCreate) -> User:
        """
        새로운 유저 생성 서비스
        Args:
            user_data (dict): 유저 생성에 필요한 데이터
        """
        existing_user = self.user_crud.get_user_by_email(user.user_email)
        if existing_user:
            logger.warning(f"❌ Email already exists: {user.user_email}")
            raise UserConflictException(user.user_email)

        if user.user_password:
            user.user_password = password_hasher.hash_password(user.user_password)
        
        created_user = self.user_crud.create(UserMapper.user_create_to_model(user))
        logger.info(f"✅ Successfully created user: {created_user.user_name} (ID: {created_user.user_id})")
        return created_user

    def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        ID로 사용자 조회
        Args:
            user_id (int): 조회할 사용자 ID
        Returns:
            UserResponse: 조회된 사용자 정보
        Raises:
            UserNotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.user_crud.get_active_user_by_id(user_id)
        if not user:
            logger.warning(f"❌ Failed to find user with id {user_id}")
            raise UserNotFoundException(user_id)
        
        logger.info(f"🙋‍♂️ Found user: {user.user_name} (ID: {user_id})")
        return UserMapper.to_dto(user)
    
    def get_user_by_email(self, user_email: str) -> UserResponse:
        """
        이메일로 사용자 조회
        Args:
            email (str): 조회할 사용자 이메일
        Returns:
            UserResponse: 조회된 사용자 정보
        Raises:
            UserNotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.user_crud.get_active_user_by_email(user_email)
        if not user:
            logger.warning(f"❌ Failed to find user with email {user_email}")
            raise UserNotFoundException(user_email)
        
        logger.info(f"🙋‍♂️ Found user by email: {user.user_name} ({user_email})")
        return UserMapper.to_dto(user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """
        사용자 정보 업데이트
        Args:
            user_id (int): 업데이트할 사용자 ID
            user_data (UserUpdate): 업데이트할 사용자 정보
        Returns:
            UserResponse: 업데이트된 사용자 정보
        Raises:
            UserNotFoundException: 사용자를 찾을 수 없는 경우
        """
        self.get_user_by_id(user_id)
        return UserMapper.to_dto(self.user_crud.update(user_id, user_data))


    def delete_user_by_id(self, user_id: int) -> bool:
        """
        사용자 삭제
        Args:
            user_id (int): 삭제할 사용자 ID
        Returns:
            bool: 삭제 성공 여부
        Raises:
            UserNotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.get_user_by_id(user_id)
        if self.user_crud.delete(user_id):
            logger.info(f"✅ Successfully deleted user: {user.user_name} (ID: {user_id})")
            return True
        return False

    def deactivate_user_by_id(self, user_id: int) -> MessageResponse:
        """
        사용자 비활성화 (soft delete)
        Args:
            user_id (int): 비활성화할 사용자 ID
        Returns:
            MessageResponse: 비활성화 성공 메세지
        Raises:
            UserNotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.get_user_by_id(user_id)
        if self.user_crud.deactivate_user(user_id):
            logger.info(f"🚫 Successfully deactivated user: {user.user_name} (ID: {user_id})")
            return MessageResponse(message="성공적으로 탈퇴 되셨습니다.")