from sqlalchemy.orm import Session

from ..core import logger
from ..crud import UserCRUD
from ..models import User
from ..mappers import UserMapper
from ..schemas import UserCreate, UserResponse
from ..exceptions import UserNotFoundException



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
        return self.user_crud.create(UserMapper.user_create_to_model(user))

    def get_user_id(self, user_id: int) -> UserResponse:
        """
        ID로 유저 조회 서비스
        Args:
            user_id: 조회할 유저의 ID
        Raises:
            HTTPException: 유저를 찾을 수 없는 경우
        """
        user = self.user_crud.get_by_id(user_id)
        if not user:
            logger.warning(f"❌ Failed to find user with id {user_id}")
            raise UserNotFoundException(user_id)
        return UserMapper.to_dto(user)