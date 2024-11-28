from fastapi.testclient import TestClient
import pytest


class TestChatLog:

    @pytest.mark.asyncio
    async def test_get_chat_logs_by_chat_id_success(self, auth_client: TestClient):
        # Set
        chat_id = 1

        # When
        response = auth_client.get(f"/api/v1/chat-log/chats/{chat_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert len(response_data) > 0

    @pytest.mark.asyncio
    async def test_delete_chat_log_success(self, auth_client: TestClient):
        # Set
        log_id = 1

        # When
        response = auth_client.delete(f"/api/v1/chat-log/{log_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "채팅 로그가 성공적으로 삭제되었습니다."
        assert response_data["data"]["log_id"] == log_id

    @pytest.mark.asyncio
    async def test_delete_chat_log_access_denied(self, auth_client: TestClient):
        # Set
        log_id = 3

        # When
        response = auth_client.delete(f"/api/v1/chat-log/{log_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 403
        assert response_data["detail"]["message"] == "자신의 채팅 로그만 삭제할 수 있습니다."
        assert response_data["detail"]["code"] == "FORBIDDEN"
        assert response_data["detail"]["log_id"] == log_id

    @pytest.mark.asyncio
    async def test_delete_chat_log_not_found(self, auth_client: TestClient):
        # Set
        log_id = 999

        # When
        response = auth_client.delete(f"/api/v1/chat-log/{log_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "채팅 로그를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["log_id"] == log_id