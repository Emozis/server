from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse

class UserMapper:
    @staticmethod
    def user_create_to_model(dto: UserCreate) -> User:
        """DTO를 Model로 변환"""
        return User(
            user_email=dto.user_email,
            user_password=dto.user_password,
            user_name=dto.user_name,
            user_profile=dto.user_profile
        )
    
    @staticmethod
    def user_update_to_model(dto: UserUpdate) -> User:
        """DTO를 Model로 변환"""
        return User(
            user_name=dto.user_name,
            user_profile=dto.user_profile,
            user_gender=dto.user_gender,
            user_birthdate=dto.user_birthdate
        )
    
    @staticmethod
    def to_dto(model: User) -> UserResponse:
        """Model을 DTO로 변환"""
        return UserResponse(
            user_id=model.user_id,
            user_email=model.user_email,
            user_name=model.user_name,
            user_profile=model.user_profile,
            user_gender=model.user_gender,
            user_birthdate=model.user_birthdate
        )