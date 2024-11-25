import pytest
from fastapi.testclient import TestClient

from app.models import User
from app.crud import UserCRUD
from app.services import AuthService

@pytest.mark.asyncio
async def test_login_success(client: TestClient):
    # Given
    login_data = {
        "userEmail": "test@example.com",
        "userPassword": "1234"
    }
    
    # When
    response = client.post("/api/v1/auth/login", json=login_data)
    
    # Then
    assert response.status_code == 200
    data: dict = response.json()
    assert data["status"] == "success"
    assert "accessToken" in data.keys()

@pytest.mark.asyncio
async def test_login_invalid_email(client: TestClient):
    # Given
    login_data = {
        "userEmail": "wrong@example.com",
        "userPassword": "wrong_password"
    }
    
    # When
    response = client.post("/api/v1/auth/login", json=login_data)
    
    # Then
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"]["message"] == "사용자를 찾을 수 없습니다."