from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from app.database.base import Base

ModelType = TypeVar("ModelType")


class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session, id_field: str):
        """
        CRUD의 기본 클래스
        Args:
            model: SQLAlchemy 모델 클래스
            db: 데이터베이스 세션
            id_field: ID 필드명 (예: 'user_id', 'image_id' 등)
        """
        self.model = model
        self.db = db
        self.id_field = id_field

    def create(self, instance: ModelType) -> ModelType:
        """
        새로운 레코드 생성
        Args:
            instance: 생성할 모델 인스턴스
        """
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create {self.model.__name__}: {str(e)}")

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        ID로 레코드 조회
        Args:
            id: 조회할 레코드의 ID
        """
        return self.db.query(self.model).filter(getattr(self.model, self.id_field) == id).first()

    def update(self, id: int, instance: ModelType) -> Optional[ModelType]:
        """
        레코드 업데이트
        Args:
            id: 업데이트할 레코드의 ID
            instance: 업데이트할 정보가 담긴 모델 인스턴스
        """
        try:
            existing_instance = self.get_by_id(id)
            if not existing_instance:
                return None

            update_data = {
                key: value
                for key, value in instance.__dict__.items()
                if not key.startswith('_') and value is not None
            }
            
            # ID 필드는 업데이트하지 않음
            update_data.pop('user_id', None)

            for key, value in update_data.items():
                setattr(existing_instance, key, value)

            self.db.commit()
            self.db.refresh(existing_instance)
            return existing_instance

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update {self.model.__name__}: {str(e)}")

    def delete(self, id: int) -> bool:
        """
        레코드 삭제
        Args:
            id: 삭제할 레코드의 ID
        """
        try:
            instance = self.get_by_id(id)
            if not instance:
                return False

            self.db.delete(instance)
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to delete {self.model.__name__}: {str(e)}")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        모든 레코드 조회
        Args:
            skip: 건너뛸 레코드 수
            limit: 조회할 최대 레코드 수
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()