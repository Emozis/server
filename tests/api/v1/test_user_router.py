import pytest
from fastapi.testclient import TestClient


class TestUser:
    test_user = {
        "userName": "test user",
        "userProfile": "profile.png",
        "userGender": "male",
        "userBirthdate": "2024-11-26T10:28:45.350Z"
    }

    @pytest.mark.asyncio
    async def test_get_user_success(self, auth_client: TestClient):
        """
        사용자 정보 조회 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 사용자 ID 일치 확인
        - 이메일 정보 일치 확인
        """
        # When
        response = auth_client.get("/api/v1/user/me")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["userId"] == 2
        assert response_data["userEmail"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_user_invalid_token(self, client: TestClient):
        """
        잘못된 토큰으로 사용자 정보 조회 시도 테스트
        
        검증 항목:
        - 401 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 토큰 확인
        """
        # Set
        token = "1234"
        
        # When
        client.headers["Authorization"] = f"Bearer {token}"
        response = client.get("/api/v1/user/me")
        response_data: dict = response.json()["detail"]
        
        # Then
        assert response.status_code == 401
        assert response_data["message"] == "유효하지 않은 인증 정보입니다."
        assert response_data["code"] == "INVALID_TOKEN"
        assert response_data["token"] == token

    @pytest.mark.asyncio
    async def test_update_user_success(self, auth_client: TestClient):
        """
        사용자 정보 수정 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 수정 성공 메시지 확인
        - 수정된 사용자 ID 확인
        """
        # Set
        data = self.test_user.copy()

        # When
        response = auth_client.put("/api/v1/user/me", json=data)
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "사용자 정보가 성공적으로 업데이트 되었습니다."
        assert response_data["data"]["userId"] == 2

    @pytest.mark.asyncio
    async def test_deactivate_user_success(self, auth_client: TestClient):
        """
        사용자 계정 비활성화 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 탈퇴 성공 메시지 확인
        - 탈퇴한 사용자 ID 확인
        """
        # When
        response = auth_client.patch("/api/v1/user/me/deactivate")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "사용자가 성공적으로 탈퇴 되었습니다."
        assert response_data["data"]["userId"] == 2
