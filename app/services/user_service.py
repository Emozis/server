from sqlalchemy.orm import Session

from ..core import logger
from ..models import User
from ..crud import UserCRUD
from ..mappers import UserMapper
from ..schemas import UserCreate, UserUpdate, UserResponse, ResponseSchema, UserIdResponse
from ..utils.password_hasher import password_hasher
from ..exceptions import NotFoundException, UserConflictException


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_crud = UserCRUD(db)

    def create_user(self, user: UserCreate) -> User:
        """
        새로운 유저 생성 서비스
        Args:
            user (UserCreate): 유저 생성에 필요한 데이터
        Returns:
            User: 생성된 유저 정보
        Raises:
            UserConflictException: 이메일이 이미 존재하는 경우
        """
        existing_user = self.user_crud.get_user_by_email(user.user_email)
        if existing_user:
            logger.warning(f"❌ Email already exists: {user.user_email}")
            raise UserConflictException(user.user_email)

        if user.user_password:
            user.user_password = password_hasher.hash_password(user.user_password)
        
        created_user = self.user_crud.create(UserMapper.user_create_to_model(user))
        logger.info(f"✨ Successfully created user: {created_user.user_name} (ID: {created_user.user_id})")
        return created_user

    def get_all_users(self) -> list[UserResponse]:
        """
        전체 사용자 목록 조회
        활성화 상태와 관계없이 데이터베이스의 모든 사용자 정보를 반환합니다.
        
        Returns:
            UserResponse: 전체 사용자 정보 목록을 포함한 DTO 객체
        """
        users = self.user_crud.get_all_users()
        return UserMapper.to_dto_list(users)

    def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        ID로 사용자 조회
        Args:
            user_id (int): 조회할 사용자 ID
        Returns:
            UserResponse: 조회된 사용자 정보
        Raises:
            NotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.user_crud.get_active_user_by_id(user_id)
        if not user:
            logger.warning(f"❌ Failed to find user with id {user_id}")
            raise NotFoundException("사용자를 찾을 수 없습니다.", "user_id", user_id)
        
        logger.info(f"🙋 Found user: {user.user_name} (ID: {user_id})")
        return UserMapper.to_dto(user)
    
    def get_user_by_email(self, user_email: str) -> UserResponse:
        """
        이메일로 사용자 조회
        Args:
            email (str): 조회할 사용자 이메일
        Returns:
            UserResponse: 조회된 사용자 정보
        Raises:
            NotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.user_crud.get_active_user_by_email(user_email)
        if not user:
            logger.warning(f"❌ Failed to find user with email {user_email}")
            raise NotFoundException("사용자를 찾을 수 없습니다.", "user_email", user_email)
        
        logger.info(f"🙋 Found user: {user.user_name} (Email: {user_email})")
        return UserMapper.to_dto(user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> ResponseSchema:
        """
        사용자 정보 업데이트
        Args:
            user_id (int): 업데이트할 사용자 ID
            user_data (UserUpdate): 업데이트할 사용자 정보
        Returns:
            ResponseSchema: 업데이트 성공 메시지와 유저 정보
        Raises:
            NotFoundException: 사용자를 찾을 수 없는 경우
        """
        self.get_user_by_id(user_id)
        updated_user = UserMapper.to_dto(self.user_crud.update(user_id, user_data))
        logger.info(f"🔄 Successfully updated user: {updated_user.user_name} (ID: {user_id})")
        return ResponseSchema(
            message="사용자 정보가 성공적으로 업데이트 되었습니다.", 
            data=UserIdResponse(user_id=updated_user.user_id, user_name=updated_user.user_name)
        )

    def delete_user_by_id(self, user_id: int) -> ResponseSchema:
        """
        사용자 완전 삭제
        Args:
            user_id (int): 삭제할 사용자 ID
        Returns:
            ResponseSchema: 삭제 성공 메시지와 유저 정보
        Raises:
            NotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.get_user_by_id(user_id)
        if self.user_crud.delete(user_id):
            logger.info(f"🗑️  Successfully deleted user: {user.user_name} (ID: {user_id})")
            return ResponseSchema(
                message="사용자가 성공적으로 삭제 되었습니다.", 
                data=UserIdResponse(user_id=user.user_id, user_name=user.user_name)
            )

    def deactivate_user_by_id(self, user_id: int) -> ResponseSchema:
        """
        사용자 비활성화 (soft delete)
        Args:
            user_id (int): 비활성화할 사용자 ID
        Returns:
            ResponseSchema: 비활성화 성공 메시지와 유저 정보
        Raises:
            NotFoundException: 사용자를 찾을 수 없는 경우
        """
        user = self.get_user_by_id(user_id)
        if self.user_crud.deactivate_user(user_id):
            logger.info(f"🚫 Successfully deactivated user: {user.user_name} (ID: {user_id})")
            return ResponseSchema(
                message="사용자가 성공적으로 탈퇴 되었습니다.", 
                data=UserIdResponse(user_id=user.user_id, user_name=user.user_name)
            )