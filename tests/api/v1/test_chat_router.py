from fastapi.testclient import TestClient
import pytest


class TestChat:
    test_chat = {
        "characterId": 1
    }
    chat_id = None

    @pytest.mark.asyncio
    async def test_create_chat_success(self, auth_client: TestClient):
        """
        채팅방 생성 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 생성 성공 메시지 확인
        - 채팅방 ID 존재 확인
        """
        # Set
        data = self.test_chat.copy()

        # When
        response = auth_client.post("/api/v1/chat", json=data)
        response_data: dict = response.json()

        TestChat.chat_id = response_data["data"]["chat_id"]
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "채팅방이 성공적으로 생성되었습니다."
        assert response_data["data"]["chat_id"]

    @pytest.mark.asyncio
    async def test_create_chat_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 캐릭터로 채팅방 생성 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        data = self.test_chat.copy()
        data["characterId"] = 999

        # When
        response = auth_client.post("/api/v1/chat", json=data)
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "캐릭터를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["character_id"] == data["characterId"]

    @pytest.mark.asyncio
    async def test_get_chat_by_user_id_success(self, auth_client: TestClient):
        """
        사용자별 채팅방 목록 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 채팅방 존재 확인
        """
        # When
        response = auth_client.get("/api/v1/chat/me")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert len(response_data) > 0

    @pytest.mark.asyncio
    async def test_delete_chat_success(self, auth_client: TestClient):
        """
        채팅방 삭제 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 삭제 성공 메시지 확인
        - 삭제된 채팅방 ID 확인
        """
        # Set
        chat_id = self.chat_id

        # When
        response = auth_client.delete(f"/api/v1/chat/{chat_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "채팅방이 성공적으로 삭제되었습니다."
        assert response_data["data"]["chat_id"] == self.chat_id

    @pytest.mark.asyncio
    async def test_delete_chat_access_denied(self, auth_client: TestClient):
        """
        타인의 채팅방 삭제 시도 테스트
        
        검증 항목:
        - 403 상태 코드 반환
        - 접근 거부 메시지 확인
        - 에러 코드 및 채팅방 ID 확인
        """
        # Set
        chat_id = 2

        # When
        response = auth_client.delete(f"/api/v1/chat/{chat_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 403
        assert response_data["detail"]["message"] == "자신의 채팅방만 삭제할 수 있습니다."
        assert response_data["detail"]["code"] == "FORBIDDEN"
        assert response_data["detail"]["chat_id"] == chat_id

    @pytest.mark.asyncio
    async def test_delete_chat_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 채팅방 삭제 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 채팅방 ID 확인
        """
        # Set
        chat_id = 999

        # When
        response = auth_client.delete(f"/api/v1/chat/{chat_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "채팅방을 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["chat_id"] == chat_id