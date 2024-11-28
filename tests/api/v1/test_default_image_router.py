import pytest
from fastapi.testclient import TestClient
import io


class TestDefaultImage:
    file = {
        "image": ("test_image.jpg", io.BytesIO(b"fake image content"), "image/jpeg")
    }
    test_default_image = {
        "gender": "male",
        "ageGroup": "youth",
        "emotion": "A"
    }
    image_id = None

    @pytest.mark.asyncio
    async def test_create_default_image_success(self, auth_client: TestClient):
        """
        기본 이미지 생성 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 생성 성공 메시지 확인
        - 이미지 ID 존재 확인
        """
        # Set
        file = self.file.copy()
        data = self.test_default_image.copy()

        # When
        response = auth_client.post(
            "/api/v1/default-image",
            files=file,
            data=data
        )
        response_data: dict = response.json()

        TestDefaultImage.image_id = response_data["data"]["image_id"]
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "기본 이미지가 성공적으로 저장되었습니다."
        assert response_data["data"]["image_id"]

    @pytest.mark.asyncio
    async def test_create_default_image_invalid_format(self, auth_client: TestClient):
        """
        잘못된 파일 형식으로 이미지 생성 시도 테스트
        
        검증 항목:
        - 415 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 콘텐츠 타입 확인
        """
        # Set
        file = self.file.copy()
        file["image"] = ("test_image.jpg", io.BytesIO(b"fake image content"), "text/plain")
        data = self.test_default_image

        # When
        response = auth_client.post(
            "/api/v1/default-image",
            files=file,
            data=data
        )
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 415
        assert response_data["detail"]["message"] == "지원하지 않는 파일 형식입니다."
        assert response_data["detail"]["code"] == "UNSUPPORTED_IMAGE_FORMAT"
        assert response_data["detail"]["content_type"] == "text/plain"

    @pytest.mark.asyncio
    async def test_create_default_image_invalid_enum(self, auth_client: TestClient):
        """
        잘못된 열거형 값으로 이미지 생성 시도 테스트
        
        검증 항목:
        - 422 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드, 필드명, 잘못된 값 확인
        """
        # Set
        file = self.file.copy()
        data = self.test_default_image.copy()
        data["gender"] = "invalid_gender"

        # When
        response = auth_client.post(
            "/api/v1/default-image",
            files=file,
            data=data
        )
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 422
        assert response_data["detail"]["message"] == "잘못된 image_gender 값입니다."
        assert response_data["detail"]["code"] == "INVALID_ENUM_VALUE"
        assert response_data["detail"]["field"] == "image_gender"
        assert response_data["detail"]["provided_value"] == "invalid_gender"

    @pytest.mark.asyncio
    async def test_get_default_images_success(self, auth_client: TestClient):
        """
        기본 이미지 목록 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 최소 10개 이상의 이미지 존재 확인
        """
        # When
        response = auth_client.get("/api/v1/default-image")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert len(response_data) >= 10

    @pytest.mark.asyncio
    async def test_get_default_image_by_id_success(self, auth_client: TestClient):
        """
        ID로 기본 이미지 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 조회된 이미지 ID 일치 확인
        """
        # Set
        image_id = self.image_id

        # When
        response = auth_client.get(f"/api/v1/default-image/{image_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["imageId"] == image_id

    @pytest.mark.asyncio
    async def test_get_default_image_by_id_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 이미지 조회 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 이미지 ID 확인
        """
        # Set
        image_id = 111

        # When
        response = auth_client.get(f"/api/v1/default-image/{image_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "이미지를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["image_id"] == image_id

    @pytest.mark.asyncio
    async def test_update_default_image_success(self, auth_client: TestClient):
        """
        기본 이미지 수정 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 수정 성공 메시지 확인
        - 수정된 이미지 ID 확인
        """
        # Set
        file = self.file.copy()
        data = self.test_default_image.copy()
        image_id = self.image_id

        # When
        response = auth_client.put(
            f"/api/v1/default-image/{image_id}",
            files=file,
            data=data
        )
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "기본 이미지가 성공적으로 수정되었습니다."
        assert response_data["data"]["image_id"] == image_id

    @pytest.mark.asyncio
    async def test_update_default_image_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 이미지 수정 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 이미지 ID 확인
        """
        # Set
        file = self.file.copy()
        data = self.test_default_image.copy()
        image_id = 999

        # When
        response = auth_client.put(
            f"/api/v1/default-image/{image_id}",
            files=file,
            data=data
        )
        response_data: dict = response.json()

        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "이미지를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["image_id"] == image_id

    @pytest.mark.asyncio
    async def test_update_default_image_invalid_formatd(self, auth_client: TestClient):
        """
        잘못된 파일 형식으로 이미지 수정 시도 테스트
        
        검증 항목:
        - 415 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 콘텐츠 타입 확인
        """
        # Set
        file = self.file.copy()
        file["image"] = ("test_image.jpg", io.BytesIO(b"fake image content"), "text/plain")
        data = self.test_default_image.copy()
        image_id = self.image_id

        # When
        response = auth_client.put(
            f"/api/v1/default-image/{image_id}",
            files=file,
            data=data
        )
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 415
        assert response_data["detail"]["message"] == "지원하지 않는 파일 형식입니다."
        assert response_data["detail"]["code"] == "UNSUPPORTED_IMAGE_FORMAT"
        assert response_data["detail"]["content_type"] == "text/plain"

    @pytest.mark.asyncio
    async def test_update_default_image_invalid_enum(self, auth_client: TestClient):
        """
        잘못된 열거형 값으로 이미지 수정 시도 테스트
        
        검증 항목:
        - 422 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드, 필드명, 잘못된 값 확인
        """
        # Set
        file = self.file.copy()
        data = self.test_default_image.copy()
        data["gender"] = "invalid_gender"
        image_id = self.image_id

        # When
        response = auth_client.put(
            f"/api/v1/default-image/{image_id}",
            files=file,
            data=data
        )
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 422
        assert response_data["detail"]["message"] == "잘못된 image_gender 값입니다."
        assert response_data["detail"]["code"] == "INVALID_ENUM_VALUE"
        assert response_data["detail"]["field"] == "image_gender"
        assert response_data["detail"]["provided_value"] == "invalid_gender"

    @pytest.mark.asyncio
    async def test_delete_default_image_success(self, auth_client: TestClient):
        """
        기본 이미지 삭제 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 삭제 성공 메시지 확인
        - 삭제된 이미지 ID 확인
        """
        # Set
        image_id = self.image_id

        # When
        response = auth_client.delete(f"/api/v1/default-image/{image_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "기본 이미지가 성공적으로 삭제되었습니다."
        assert response_data["data"]["image_id"] == image_id

    @pytest.mark.asyncio
    async def test_delete_default_image_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 이미지 삭제 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 이미지 ID 확인
        """
        # Set
        image_id = 999

        # When
        response = auth_client.delete(f"/api/v1/default-image/{image_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "이미지를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["image_id"] == image_id
