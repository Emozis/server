import pytest
from fastapi.testclient import TestClient


class TestAuth:
    test_user = {
        "userEmail": "test@example.com",
        "userPassword": "1234"
    }
    user_id = None

    @pytest.mark.asyncio
    async def test_login_success(self, client: TestClient):
        """
        유효한 인증 정보로 로그인 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 응답에 성공 상태 포함
        - 액세스 토큰 포함 여부
        - 후속 테스트를 위한 사용자 ID 저장
        """
        # Given
        data = self.test_user.copy()
        
        # When
        response = client.post("/api/v1/auth/login", json=data)
        response_data: dict = response.json()

        TestAuth.user_id = response_data["user"]["userId"]

        # Then
        assert response.status_code == 200
        assert response_data["status"] == "success"
        assert "accessToken" in response_data.keys()

    @pytest.mark.asyncio
    async def test_login_invalid_email(self, client: TestClient):
        """
        잘못된 이메일로 로그인 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 오류 상세 정보 포함
        - '사용자를 찾을 수 없습니다' 메시지 확인
        """
        # Given
        data = self.test_user.copy()
        data["userEmail"] = "wrong@example.com"
        data["userPassword"] = "wrong_password"
        
        # When
        response = client.post("/api/v1/auth/login", json=data)
        response_data = response.json()
        
        # Then
        assert response.status_code == 404
        assert "detail" in response_data
        assert response_data["detail"]["message"] == "사용자를 찾을 수 없습니다."

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client: TestClient):
        """
        잘못된 비밀번호로 로그인 시도 테스트
        
        검증 항목:
        - 401 상태 코드 반환
        - 오류 상세 정보 포함
        - '비밀번호가 일치하지 않습니다' 메시지 확인
        """
        # Given
        data = self.test_user.copy()
        data["userPassword"] = "12345"
        
        # When
        response = client.post("/api/v1/auth/login", json=data)
        response_data = response.json()
        
        # Then
        assert response.status_code == 401
        assert "detail" in response_data
        assert response_data["detail"]["message"] == "비밀번호가 일치하지 않습니다."

    @pytest.mark.asyncio
    async def test_login_test_endpoint(self, client: TestClient):
        """
        테스트용 로그인 엔드포인트 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 응답에 성공 상태 포함
        - 테스트용 액세스 토큰 포함 여부
        """
        # When
        response = client.post("/api/v1/auth/login/test")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["status"] == "success"
        assert "accessToken" in response_data.keys()
