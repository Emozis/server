from fastapi.testclient import TestClient
import pytest


class TestCharacter:
    test_character = {
            "characterName": "test character",
            "characterProfile": "test",
            "characterGender": "male",
            "characterPersonality": "string",
            "characterDetails": "string",
            "characterDescription": "string",
            "characterGreeting": "string",
            "characterIsPublic": True,
            "relationships": [1, 2]
        }
    character_id = None

    @pytest.mark.asyncio
    async def test_create_character_success(self, auth_client: TestClient):
        """
        캐릭터 생성 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 성공 메시지 확인
        - 생성된 캐릭터 ID 존재 확인
        """
        # Set
        data = self.test_character

        # When
        response = auth_client.post("/api/v1/character", json=data)
        response_data: dict = response.json()

        TestCharacter.character_id = response_data["data"]["characterId"]
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "캐릭터가 성공적으로 생성되었습니다."
        assert response_data["data"]["characterId"]

    @pytest.mark.asyncio
    async def test_get_public_characters_success(self, auth_client: TestClient):
        """
        공개 캐릭터 목록 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 생성된 캐릭터 존재 확인
        - 캐릭터 정보 일치 여부 확인
        """
        # When
        response = auth_client.get("/api/v1/character")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        character = [char for char in response_data if char["characterId"] == self.character_id]
        assert character
        assert character[0]["characterName"] == self.test_character["characterName"]
        assert character[0]["characterGender"] == self.test_character["characterGender"]

    @pytest.mark.asyncio
    async def test_get_public_characters_public(self, auth_client: TestClient):
        """
        비공개 캐릭터 목록 제외 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 비공개 캐릭터 미포함 확인
        """
        # Set
        data = self.test_character.copy()
        data["characterIsPublic"] = False

        response = auth_client.post("/api/v1/character", json=data)
        response_data: dict = response.json()
        not_public_character_id = response_data["data"]["characterId"]

        # When
        response = auth_client.get("/api/v1/character")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        character = [char for char in response_data if char["characterId"] == not_public_character_id]
        assert len(character) == 0

    @pytest.mark.asyncio
    async def test_get_top_used_public_characters_success(self, auth_client: TestClient):
        """
        인기 캐릭터 상위 5개 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 정확히 5개의 캐릭터 반환 확인
        """
        # When
        response = auth_client.get("/api/v1/character/rank")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert len(response_data) == 5

    @pytest.mark.asyncio
    async def test_get_characters_by_user_id_success(self, auth_client: TestClient):
        """
        사용자별 캐릭터 목록 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 사용자의 캐릭터 2개 존재 확인
        """
        # When
        response = auth_client.get("/api/v1/character/me")
        response_data: dict = response.json()
        # Then
        assert response.status_code == 200
        assert len(response_data) == 2

    @pytest.mark.asyncio
    async def test_get_character_by_id_success(self, auth_client: TestClient):
        """
        캐릭터 상세 정보 조회 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 캐릭터 정보 일치 확인
        - 관계 정보 일치 확인
        """
        # When
        response = auth_client.get(f"/api/v1/character/{self.character_id}")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert response_data["characterName"] == self.test_character["characterName"]
        assert response_data["characterGender"] == self.test_character["characterGender"]
        assert [relationship["relationshipId"] for relationship in response_data["characterRelationships"]] == self.test_character["relationships"]

    @pytest.mark.asyncio
    async def test_get_character_by_id_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 캐릭터 조회 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        character_id = 999
        
        # When
        response = auth_client.get(f"/api/v1/character/{character_id}")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "캐릭터를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_update_character_success(self, auth_client: TestClient):
        """
        캐릭터 정보 수정 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 수정 성공 메시지 확인
        - 수정된 캐릭터 ID 확인
        """
        # Set
        data = self.test_character.copy()
        data["characterName"] = "updated test character"
        data["characterProfile"] = "updated profile"
        data["characterGender"] = "female"

        # When
        response = auth_client.put(f"/api/v1/character/{self.character_id}", json=data)
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert response_data["message"] == "캐릭터가 성공적으로 수정되었습니다."
        assert response_data["data"]["characterId"] == self.character_id

    @pytest.mark.asyncio
    async def test_update_character_access_denied(self, auth_client: TestClient):
        """
        타인의 캐릭터 수정 시도 테스트
        
        검증 항목:
        - 403 상태 코드 반환
        - 접근 거부 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        character_id = 2
        data = self.test_character.copy()
        data["characterName"] = "updated test character"
        data["characterProfile"] = "updated profile"
        data["characterGender"] = "female"

        # When
        response = auth_client.put(f"/api/v1/character/{character_id}", json=data)
        response_data: dict = response.json()

        # Then
        assert response.status_code == 403
        assert response_data["detail"]["message"] == "자신의 캐릭터만 수정할 수 있습니다."
        assert response_data["detail"]["code"] == "FORBIDDEN"
        assert response_data["detail"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_update_character_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 캐릭터 수정 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        character_id = 999
        data = self.test_character.copy()
        data["characterName"] = "updated test character"
        data["characterProfile"] = "updated profile"
        data["characterGender"] = "female"

        # When
        response = auth_client.put(f"/api/v1/character/{character_id}", json=data)
        response_data: dict = response.json()

        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "캐릭터를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_deactivate_character_success(self, auth_client: TestClient):
        """
        캐릭터 비활성화 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 비활성화 성공 메시지 확인
        - 비활성화된 캐릭터 ID 확인
        """
        # Set
        character_id = self.character_id

        # When
        response = auth_client.patch(f"/api/v1/character/{character_id}/deactive")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert response_data["message"] == "성공적으로 캐릭터를 비활성화 하였습니다."
        assert response_data["data"]["characterId"] == character_id

    @pytest.mark.asyncio
    async def test_deactivate_character_access_denied(self, auth_client: TestClient):
        """
        타인의 캐릭터 비활성화 시도 테스트
        
        검증 항목:
        - 403 상태 코드 반환
        - 접근 거부 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        character_id = 2

        # When
        response = auth_client.patch(f"/api/v1/character/{character_id}/deactive")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 403
        assert response_data["detail"]["message"] == "자신의 캐릭터만 비활성화할 수 있습니다."
        assert response_data["detail"]["code"] == "FORBIDDEN"
        assert response_data["detail"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_deactivate_character_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 캐릭터 비활성화 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        character_id = 999

        # When
        response = auth_client.patch(f"/api/v1/character/{character_id}/deactive")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "캐릭터를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_delete_character_success(self, auth_client: TestClient):
        """
        캐릭터 삭제 성공 테스트
        
        검증 항목:
        - 200 상태 코드 반환
        - 삭제 성공 메시지 확인
        - 삭제된 캐릭터 ID 확인
        """
        # Set
        character_id = self.character_id

        # When
        response = auth_client.delete(f"/api/v1/character/{character_id}")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert response_data["message"] == "캐릭터가 성공적으로 삭제되었습니다."
        assert response_data["data"]["characterId"] == character_id

    @pytest.mark.asyncio
    async def test_delete_character_access_denied(self, auth_client: TestClient):
        """
        타인의 캐릭터 삭제 시도 테스트
        
        검증 항목:
        - 403 상태 코드 반환
        - 접근 거부 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        character_id = 2

        # When
        response = auth_client.delete(f"/api/v1/character/{character_id}")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 403
        assert response_data["detail"]["message"] == "자신의 캐릭터만 삭제할 수 있습니다."
        assert response_data["detail"]["code"] == "FORBIDDEN"
        assert response_data["detail"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_delete_character_not_found(self, auth_client: TestClient):
        """
        존재하지 않는 캐릭터 삭제 시도 테스트
        
        검증 항목:
        - 404 상태 코드 반환
        - 에러 메시지 확인
        - 에러 코드 및 캐릭터 ID 확인
        """
        # Set
        character_id = 999

        # When
        response = auth_client.delete(f"/api/v1/character/{character_id}")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 404
        assert response_data["detail"]["message"] == "캐릭터를 찾을 수 없습니다."
        assert response_data["detail"]["code"] == "NOT_FOUND"
        assert response_data["detail"]["character_id"] == character_id