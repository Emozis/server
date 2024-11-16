from sqlalchemy.orm import Session

from ..core import logger
from ..crud import UserCRUD
from ..mappers import UserMapper
from ..schemas import UserUpdate, UserResponse, MessageResponse
from ..exceptions import (
    UserNotFoundException
)


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_crud = UserCRUD(db)

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
        self.get_user_by_id(user_id)
        return self.user_crud.delete(user_id)

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
        self.get_user_by_id(user_id)
        if self.user_crud.deactivate_user(user_id):
            return MessageResponse(message="성공적으로 탈퇴 되셨습니다.")