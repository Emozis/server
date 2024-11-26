import pytest
from fastapi.testclient import TestClient
import io


@pytest.fixture
def sample_image():
    return io.BytesIO(b"fake image content")

@pytest.mark.asyncio
async def test_create_default_image_success(auth_client: TestClient, sample_image):
    # Set
    files = {
        "image": ("test_image.jpg", sample_image, "image/jpeg")
    }
    
    data = {
        "gender": "male",
        "ageGroup": "youth",
        "emotion": "A"
    }

    # When
    response = auth_client.post(
        "/api/v1/default-image",
        files=files,
        data=data
    )
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "기본 이미지가 성공적으로 저장되었습니다."
    assert data["data"]["image_id"]

@pytest.mark.asyncio
async def test_create_default_image_invalid_format(auth_client: TestClient, sample_image):
    # Set
    files = {
        "image": ("test_image.jpg", sample_image, "text/plain")
    }
    
    data = {
        "gender": "male",
        "ageGroup": "youth",
        "emotion": "A"
    }

    # When
    response = auth_client.post(
        "/api/v1/default-image",
        files=files,
        data=data
    )
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 415
    assert data["detail"]["message"] == "지원하지 않는 파일 형식입니다."
    assert data["detail"]["code"] == "UNSUPPORTED_IMAGE_FORMAT"
    assert data["detail"]["content_type"] == "text/plain"

@pytest.mark.asyncio
async def test_create_default_image_invalid_enum(auth_client: TestClient, sample_image):
    # Set
    files = {
        "image": ("test_image.jpg", sample_image, "image/jpeg")
    }
    
    data = {
        "gender": "invalid_gender",
        "ageGroup": "youth",
        "emotion": "A"
    }

    # When
    response = auth_client.post(
        "/api/v1/default-image",
        files=files,
        data=data
    )
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 422
    assert data["detail"]["message"] == "잘못된 image_gender 값입니다."
    assert data["detail"]["code"] == "INVALID_ENUM_VALUE"
    assert data["detail"]["field"] == "image_gender"
    assert data["detail"]["provided_value"] == "invalid_gender"

@pytest.mark.asyncio
async def test_get_default_images_success(auth_client: TestClient):
    # When
    response = auth_client.get("/api/v1/default-image")
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 200
    assert len(data) >= 10

@pytest.mark.asyncio
async def test_get_default_image_by_id_success(auth_client: TestClient):
    # Set
    image_id = 1

    # When
    response = auth_client.get(f"/api/v1/default-image/{image_id}")
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 200
    assert data["imageId"] == image_id

@pytest.mark.asyncio
async def test_get_default_image_by_id_not_found(auth_client: TestClient):
    # Set
    image_id = 111

    # When
    response = auth_client.get(f"/api/v1/default-image/{image_id}")
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 404
    assert data["detail"]["message"] == "이미지를 찾을 수 없습니다."
    assert data["detail"]["code"] == "NOT_FOUND"
    assert data["detail"]["image_id"] == image_id

@pytest.mark.asyncio
async def test_update_default_image_success(auth_client: TestClient, sample_image):
    # Set
    image_id = 1
    files = {
        "image": ("test_image.jpg", sample_image, "image/jpeg")
    }
    
    data = {
        "gender": "male",
        "ageGroup": "youth",
        "emotion": "A"
    }

    # When
    response = auth_client.put(
        f"/api/v1/default-image/{image_id}",
        files=files,
        data=data
    )
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "기본 이미지가 성공적으로 수정되었습니다."
    assert data["data"]["image_id"] == image_id

@pytest.mark.asyncio
async def test_update_default_image_not_found(auth_client: TestClient, sample_image):
    # Set
    image_id = 111
    files = {
        "image": ("test_image.jpg", sample_image, "image/jpeg")
    }
    
    data = {
        "gender": "male",
        "ageGroup": "youth",
        "emotion": "A"
    }

    # When
    response = auth_client.put(
        f"/api/v1/default-image/{image_id}",
        files=files,
        data=data
    )
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 404
    assert data["detail"]["message"] == "이미지를 찾을 수 없습니다."
    assert data["detail"]["code"] == "NOT_FOUND"
    assert data["detail"]["image_id"] == image_id

@pytest.mark.asyncio
async def test_update_default_image_invalid_formatd(auth_client: TestClient, sample_image):
    # Set
    image_id = 111
    files = {
        "image": ("test_image.jpg", sample_image, "text/plain")
    }
    
    data = {
        "gender": "male",
        "ageGroup": "youth",
        "emotion": "A"
    }

    # When
    response = auth_client.put(
        f"/api/v1/default-image/{image_id}",
        files=files,
        data=data
    )
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 415
    assert data["detail"]["message"] == "지원하지 않는 파일 형식입니다."
    assert data["detail"]["code"] == "UNSUPPORTED_IMAGE_FORMAT"
    assert data["detail"]["content_type"] == "text/plain"

@pytest.mark.asyncio
async def test_update_default_image_invalid_enum(auth_client: TestClient, sample_image):
    # Set
    image_id = 111
    files = {
        "image": ("test_image.jpg", sample_image, "image/jpeg")
    }
    
    data = {
        "gender": "invalid_gender",
        "ageGroup": "youth",
        "emotion": "A"
    }

    # When
    response = auth_client.put(
        f"/api/v1/default-image/{image_id}",
        files=files,
        data=data
    )
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 422
    assert data["detail"]["message"] == "잘못된 image_gender 값입니다."
    assert data["detail"]["code"] == "INVALID_ENUM_VALUE"
    assert data["detail"]["field"] == "image_gender"
    assert data["detail"]["provided_value"] == "invalid_gender"

@pytest.mark.asyncio
async def test_delete_default_image_success(auth_client: TestClient):
    # Set
    image_id = 1

    # When
    response = auth_client.delete(f"/api/v1/default-image/{image_id}")
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 200
    assert data["message"] == "기본 이미지가 성공적으로 삭제되었습니다."
    assert data["data"]["image_id"] == image_id

@pytest.mark.asyncio
async def test_delete_default_image_not_found(auth_client: TestClient):
    # Set
    image_id = 111

    # When
    response = auth_client.delete(f"/api/v1/default-image/{image_id}")
    data: dict = response.json()
    print(data)
    
    # Then
    assert response.status_code == 404
    assert data["detail"]["message"] == "이미지를 찾을 수 없습니다."
    assert data["detail"]["code"] == "NOT_FOUND"
    assert data["detail"]["image_id"] == image_id
