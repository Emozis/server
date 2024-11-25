import pytest
from fastapi.testclient import TestClient

from app.models import User
from app.crud import UserCRUD
from app.services import AuthService

@pytest.mark.asyncio
async def test_get_user_success(auth_client: TestClient):
    # When
    response = auth_client.get("/api/v1/user/me")
    
    # Then
    assert response.status_code == 200
    data: dict = response.json()
    assert data["userId"] == 2
    assert data["userEmail"] == "test@example.com"

@pytest.mark.asyncio
async def test_get_user_invalid_token(client: TestClient):
    # When
    token = "1234"
    client.headers["Authorization"] = f"Bearer {token}"
    response = client.get("/api/v1/user/me")
    
    # Then
    assert response.status_code == 401
    data: dict = response.json()["detail"]
    assert data["message"] == "유효하지 않은 인증 정보입니다."
    assert data["code"] == "INVALID_TOKEN"
    assert data["details"]["token"] == token

# @pytest.mark.asyncio
# async def test_login_invalid_email(client: TestClient):
#     # Given
#     login_data = {
#         "userEmail": "wrong@example.com",
#         "userPassword": "wrong_password"
#     }
    
#     # When
#     response = client.post("/api/v1/auth/login", json=login_data)
    
#     # Then
#     assert response.status_code == 404
#     data = response.json()
#     assert "detail" in data
#     assert data["detail"]["message"] == "사용자를 찾을 수 없습니다."

# @pytest.mark.asyncio
# async def test_login_invalid_password(client: TestClient):
#     # Given
#     login_data = {
#         "userEmail": "test@example.com",
#         "userPassword": "12345"
#     }
    
#     # When
#     response = client.post("/api/v1/auth/login", json=login_data)
    
#     # Then
#     assert response.status_code == 401
#     data = response.json()
#     assert "detail" in data
#     assert data["detail"]["message"] == "비밀번호가 일치하지 않습니다."



# @pytest.mark.asyncio
# async def test_login_test_endpoint(client: TestClient):
#     # When
#     response = client.post("/api/v1/auth/login/test")
    
#     # Then
#     assert response.status_code == 200
#     data: dict = response.json()
#     assert data["status"] == "success"
#     assert "accessToken" in data.keys()

# # Optional: Helper fixture for authenticated client
# @pytest.fixture
# def auth_client(client, db_session):
#     """인증된 테스트 클라이언트를 반환하는 fixture"""
#     # Login and get token
#     response = client.post("/api/v1/auth/login", json={
#         "email": "test@example.com",
#         "password": "1234"
#     })
#     token = response.json()["access_token"]
    
#     # Add token to headers
#     client.headers["Authorization"] = f"Bearer {token}"
#     return client