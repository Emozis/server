import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_user_success(auth_client: TestClient):
    # When
    response = auth_client.get("/api/v1/user/me")
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert data["userId"] == 2
    assert data["userEmail"] == "test@example.com"

@pytest.mark.asyncio
async def test_get_user_invalid_token(client: TestClient):
    # Set
    token = "1234"
    
    # When
    client.headers["Authorization"] = f"Bearer {token}"
    response = client.get("/api/v1/user/me")
    data: dict = response.json()["detail"]
    
    # Then
    assert response.status_code == 401
    assert data["message"] == "유효하지 않은 인증 정보입니다."
    assert data["code"] == "INVALID_TOKEN"
    assert data["token"] == token

@pytest.mark.asyncio
async def test_update_user_success(auth_client: TestClient):
    # Set
    update_data = {
        "userName": "string",
        "userProfile": "string",
        "userGender": "male",
        "userBirthdate": "2024-11-26T10:28:45.350Z"
    }

    # When
    response = auth_client.put("/api/v1/user/me", json=update_data)
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "사용자 정보가 성공적으로 업데이트 되었습니다."
    assert data["data"]["user_id"] == 2

@pytest.mark.asyncio
async def test_deactivate_user_success(auth_client: TestClient):
    # When
    response = auth_client.patch("/api/v1/user/me/deactivate")
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "사용자가 성공적으로 탈퇴 되었습니다."
    assert data["data"]["user_id"] == 2
