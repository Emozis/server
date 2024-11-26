import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_relationship_success(auth_client: TestClient):
    # Set
    data = {
        "relationshipName": "test"
    }

    # When
    response = auth_client.post("/api/v1/relationship", json=data)
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "관계가 성공적으로 생성되었습니다."
    assert data["data"]["relationship_id"]

@pytest.mark.asyncio
async def test_get_relationships_success(auth_client: TestClient):
    # When
    response = auth_client.get("/api/v1/relationship")
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert len(data) == 10
    assert data[0]["relationshipName"] == "연인"

@pytest.mark.asyncio
async def test_get_relationship_by_id_success(auth_client: TestClient):
    # Set
    relationship_id = 1

    # When
    response = auth_client.get(f"/api/v1/relationship/{relationship_id}")
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert data["relationshipId"] == relationship_id
    assert data["relationshipName"] == "연인"

@pytest.mark.asyncio
async def test_get_relationship_by_id_not_found(auth_client: TestClient):
    # Set
    relationship_id = 111

    # When
    response = auth_client.get(f"/api/v1/relationship/{relationship_id}")
    data: dict = response.json()
    
    # Then
    assert response.status_code == 404
    assert data["detail"]["message"] == "관계를 찾을 수 없습니다."
    assert data["detail"]["code"] == "NOT_FOUND"
    assert data["detail"]["relationship_id"] == relationship_id

@pytest.mark.asyncio
async def test_update_relationship_success(auth_client: TestClient):
    # Set
    relationship_id = 1
    data = {
        "relationshipName": "update"
    }

    # When
    response = auth_client.put(f"/api/v1/relationship/{relationship_id}", json=data)
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "관계가 성공적으로 수정되었습니다."
    assert data["data"]["relationship_id"] == relationship_id

@pytest.mark.asyncio
async def test_update_relationship_not_found(auth_client: TestClient):
    # Set
    relationship_id = 111
    data = {
        "relationshipName": "update"
    }

    # When
    response = auth_client.put(f"/api/v1/relationship/{relationship_id}", json=data)
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 404
    assert data["detail"]["message"] == "관계를 찾을 수 없습니다."
    assert data["detail"]["code"] == "NOT_FOUND"
    assert data["detail"]["relationship_id"] == relationship_id

@pytest.mark.asyncio
async def test_delete_relationship_success(auth_client: TestClient):
    # Set
    relationship_id = 1

    # When
    response = auth_client.delete(f"/api/v1/relationship/{relationship_id}")
    data: dict = response.json()
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "관계가 성공적으로 삭제되었습니다."
    assert data["data"]["relationship_id"] == relationship_id

@pytest.mark.asyncio
async def test_delete_relationship_not_found(auth_client: TestClient):
    # Set
    relationship_id = 111

    # When
    response = auth_client.delete(f"/api/v1/relationship/{relationship_id}")
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 404
    assert data["detail"]["message"] == "관계를 찾을 수 없습니다."
    assert data["detail"]["code"] == "NOT_FOUND"
    assert data["detail"]["relationship_id"] == relationship_id
