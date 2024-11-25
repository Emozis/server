# import pytest
# from datetime import datetime

# from app.models import User
# from app.crud.user_crud import UserCRUD

# @pytest.mark.asyncio
# async def test_create_user(db_session):
#     # Given
#     user_crud = UserCRUD(db_session)
#     test_user = User(
#         user_email="test@example.com",
#         user_password="test_password",
#         user_name="Test User",
#         user_profile="test_profile.jpg",
#         user_gender="other",
#         user_birthdate=datetime(2000, 1, 1)
#     )
    
#     # When
#     created_user = user_crud.create(test_user)
    
#     # Then
#     assert created_user.user_id is not None
#     assert created_user.user_email == "test@example.com"

# @pytest.mark.asyncio
# async def test_get_user_by_id(db_session):
#     # Given
#     user_crud = UserCRUD(db_session)
#     test_user = User(
#         user_email="test@example.com",
#         user_password="test_password",
#         user_name="Test User"
#     )
#     created_user = user_crud.create(test_user)
    
#     # When
#     fetched_user = user_crud.get_by_id(created_user.user_id)
    
#     # Then
#     assert fetched_user is not None
#     assert fetched_user.user_email == created_user.user_email

# @pytest.mark.asyncio
# async def test_update_user(db_session):
#     # Given
#     user_crud = UserCRUD(db_session)
#     test_user = User(
#         user_email="test@example.com",
#         user_password="test_password",
#         user_name="Test User"
#     )
#     created_user = user_crud.create(test_user)
    
#     # When
#     update_data = User(
#         user_name="Updated Name",
#         user_profile="updated_profile.jpg"
#     )
#     updated_user = user_crud.update(created_user.user_id, update_data)
    
#     # Then
#     assert updated_user is not None
#     assert updated_user.user_name == "Updated Name"
#     assert updated_user.user_email == "test@example.com"

# @pytest.mark.asyncio
# async def test_delete_user(db_session):
#     # Given
#     user_crud = UserCRUD(db_session)
#     test_user = User(
#         user_email="test@example.com",
#         user_password="test_password",
#         user_name="Test User"
#     )
#     created_user = user_crud.create(test_user)
    
#     # When
#     result = user_crud.delete(created_user.user_id)
    
#     # Then
#     assert result is True
#     assert user_crud.get_by_id(created_user.user_id) is None

# # API 테스트
# @pytest.mark.asyncio
# async def test_create_user_api(client, db_session):
#     # Given
#     user_data = {
#         "user_email": "test@example.com",
#         "user_password": "test_password",
#         "user_name": "Test User",
#         "user_profile": "test_profile.jpg",
#         "user_gender": "other",
#         "user_birthdate": "2000-01-01"
#     }
    
#     # When
#     response = client.post("/api/v1/users/", json=user_data)
    
#     # Then
#     assert response.status_code == 200
#     data = response.json()
#     assert data["user_email"] == user_data["user_email"]