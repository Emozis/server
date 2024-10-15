# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session

# from app.models.users import User  # 실제 모델로 교체
# from app.schemas.user.user_update_request import UserUpdate  # 실제 스키마로 교체
# from app.crud.user_crud import (
#     get_all_users, 
#     get_user_by_id, 
#     get_user_by_email, 
#     update_user_by_id, 
#     delete_user_by_id, 
#     deactivate_user_by_id
# )

# # In-memory SQLite 데이터베이스 설정
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# @pytest.fixture(scope="function")
# def db():
#     """각 테스트에서 사용할 임시 DB 세션을 설정합니다."""
#     Base.metadata.create_all(bind=engine)
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)

# # 사용자 더미 데이터 생성 함수
# def create_dummy_user(db: Session, email="test@example.com", is_active=True):
#     user = User(user_email=email, user_is_active=is_active)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# # 테스트: 모든 사용자 조회
# def test_get_all_users(db):
#     # 사용자 생성
#     user1 = create_dummy_user(db, "user1@example.com")
#     user2 = create_dummy_user(db, "user2@example.com")

#     # 테스트 함수 호출
#     users = get_all_users(db)

#     assert len(users) == 2
#     assert users[0].user_email == "user1@example.com"
#     assert users[1].user_email == "user2@example.com"

# # 테스트: ID로 사용자 조회
# def test_get_user_by_id(db):
#     # 사용자 생성
#     user = create_dummy_user(db, "user@example.com")

#     # 테스트 함수 호출
#     found_user = get_user_by_id(user.user_id, db)

#     assert found_user is not None
#     assert found_user.user_email == "user@example.com"

# # 테스트: 이메일로 사용자 조회
# def test_get_user_by_email(db):
#     # 사용자 생성
#     user = create_dummy_user(db, "user@example.com")

#     # 테스트 함수 호출
#     found_user = get_user_by_email("user@example.com", db)

#     assert found_user is not None
#     assert found_user.user_email == "user@example.com"

# # 테스트: 사용자 정보 업데이트
# def test_update_user_by_id(db):
#     # 사용자 생성
#     user = create_dummy_user(db, "user@example.com")

#     # 업데이트할 데이터 준비
#     user_update = UserUpdate(user_email="updated@example.com")

#     # 테스트 함수 호출
#     updated_user = update_user_by_id(user.user_id, user_update, db)

#     assert updated_user is not None
#     assert updated_user.user_email == "updated@example.com"

# # 테스트: 사용자 삭제
# def test_delete_user_by_id(db):
#     # 사용자 생성
#     user = create_dummy_user(db, "user@example.com")

#     # 테스트 함수 호출
#     deleted = delete_user_by_id(user.user_id, db)

#     assert deleted is True

#     # 삭제된 사용자가 존재하지 않는지 확인
#     found_user = get_user_by_id(user.user_id, db)
#     assert found_user is None

# # 테스트: 사용자 비활성화
# def test_deactivate_user_by_id(db):
#     # 사용자 생성
#     user = create_dummy_user(db, "user@example.com")

#     # 테스트 함수 호출
#     deactivated_user = deactivate_user_by_id(user.user_id, db)

#     assert deactivated_user is not None
#     assert deactivated_user.user_is_active is False
#     assert deactivated_user.user_email is None
