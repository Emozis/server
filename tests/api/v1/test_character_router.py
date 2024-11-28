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
        # Set
        data = self.test_character

        # When
        response = auth_client.post("/api/v1/character", json=data)
        response_data: dict = response.json()

        TestCharacter.character_id = response_data["data"]["character_id"]
        
        # Then
        assert response.status_code == 200
        assert response_data["message"] == "캐릭터가 성공적으로 생성되었습니다."
        assert response_data["data"]["character_id"]

    @pytest.mark.asyncio
    async def test_get_public_characters_success(self, auth_client: TestClient):
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
        # Set
        data = self.test_character.copy()
        data["characterIsPublic"] = False

        response = auth_client.post("/api/v1/character", json=data)
        response_data: dict = response.json()
        not_public_character_id = response_data["data"]["character_id"]

        # When
        response = auth_client.get("/api/v1/character")
        response_data: dict = response.json()
        
        # Then
        assert response.status_code == 200
        character = [char for char in response_data if char["characterId"] == not_public_character_id]
        assert len(character) == 0

    @pytest.mark.asyncio
    async def test_get_top_used_public_characters_success(self, auth_client: TestClient):
        # When
        response = auth_client.get("/api/v1/character/rank")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert len(response_data) == 5

    @pytest.mark.asyncio
    async def test_get_characters_by_user_id_success(self, auth_client: TestClient):
        # When
        response = auth_client.get("/api/v1/character/me")
        response_data: dict = response.json()
        # Then
        assert response.status_code == 200
        assert len(response_data) == 2

    @pytest.mark.asyncio
    async def test_get_character_by_id_success(self, auth_client: TestClient):
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
        assert response_data["data"]["character_id"] == self.character_id

    @pytest.mark.asyncio
    async def test_update_character_access_denied(self, auth_client: TestClient):
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
        # Set
        character_id = self.character_id

        # When
        response = auth_client.patch(f"/api/v1/character/{character_id}/deactive")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert response_data["message"] == "성공적으로 캐릭터를 비활성화 하였습니다."
        assert response_data["data"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_deactivate_character_access_denied(self, auth_client: TestClient):
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
        # Set
        character_id = self.character_id

        # When
        response = auth_client.delete(f"/api/v1/character/{character_id}")
        response_data: dict = response.json()

        # Then
        assert response.status_code == 200
        assert response_data["message"] == "캐릭터가 성공적으로 삭제되었습니다."
        assert response_data["data"]["character_id"] == character_id

    @pytest.mark.asyncio
    async def test_delete_character_access_denied(self, auth_client: TestClient):
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