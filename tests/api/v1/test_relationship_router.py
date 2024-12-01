import pytest
from fastapi.testclient import TestClient


class TestRelationship:
    test_relationship = {
        "relationshipName": "test"
    }
    relationship_id = None

    @pytest.mark.asyncio
    async def test_create_relationship_success(self, auth_client: TestClient):
        """
        관계 생성 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 생성 성공 메시지 확인
        - 관계 ID 존재 확인
        """
        # Set
        data = self.test_relationship.copy()

        # When
        response = auth_client.post("/api/v1/relationship", json=data)
        response_data: dict = response.json()

        TestRelationship.relationship_id = response_data["data"]["relationshipId"]
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "관계가 성공적으로 생성되었습니다."
        assert response_data["data"]["relationshipId"]

    @pytest.mark.asyncio
    async def test_get_relationships_success(self, auth_client: TestClient):
        """
        관계 목록 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 정확히 10개의 관계 확인
        - 첫 번째 관계명 확인
        """
        # When
        response = auth_client.get("/api/v1/relationship")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert len(response_data) == 10
        assert response_data[0]["relationshipName"] == "연인"

    @pytest.mark.asyncio
    async def test_get_relationship_by_id_success(self, auth_client: TestClient):
        """
        ID로 관계 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 관계 ID 일치 확인
        - 관계명 일치 확인
        """
        # Set
        relationship_id = self.relationship_id

        # When
        response = auth_client.get(f"/api/v1/relationship/{relationship_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["relationshipId"] == relationship_id
        assert response_data["relationshipName"] == self.test_relationship["relationshipName"]

    @pytest.mark.asyncio
    async def test_get_relationship_by_id_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 관계 조회 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 관계 ID 확인
        """
        # Set
        relationship_id = 999

        # When
        response = auth_client.get(f"/api/v1/relationship/{relationship_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "관계를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["relationship_id"] == relationship_id

    @pytest.mark.asyncio
    async def test_update_relationship_success(self, auth_client: TestClient):
        """
        관계 수정 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 수정 성공 메시지 확인
        - 수정된 관계 ID 확인
        """
        # Set
        data = self.test_relationship.copy()
        data["relationshipName"] = "update"
        relationship_id = self.relationship_id

        # When
        response = auth_client.put(f"/api/v1/relationship/{relationship_id}", json=data)
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "관계가 성공적으로 수정되었습니다."
        assert response_data["data"]["relationshipId"] == relationship_id

    @pytest.mark.asyncio
    async def test_update_relationship_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 관계 수정 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 관계 ID 확인
        """
        # Set
        data = self.test_relationship.copy()
        data["relationshipName"] = "update"
        relationship_id = 999

        # When
        response = auth_client.put(f"/api/v1/relationship/{relationship_id}", json=data)
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "관계를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["relationship_id"] == relationship_id

    @pytest.mark.asyncio
    async def test_delete_relationship_success(self, auth_client: TestClient):
        """
        관계 삭제 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 삭제 성공 메시지 확인
        - 삭제된 관계 ID 확인
        """
        # Set
        relationship_id = self.relationship_id

        # When
        response = auth_client.delete(f"/api/v1/relationship/{relationship_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "관계가 성공적으로 삭제되었습니다."
        assert response_data["data"]["relationshipId"] == relationship_id

    @pytest.mark.asyncio
    async def test_delete_relationship_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 관계 삭제 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 관계 ID 확인
        """
        # Set
        relationship_id = 999

        # When
        response = auth_client.delete(f"/api/v1/relationship/{relationship_id}")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "관계를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["relationship_id"] == relationship_id
