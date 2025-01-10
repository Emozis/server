from sqlalchemy.orm import Session

from ..core import logger
from ..models import CharacterRelationship
from ..crud import CharacterCRUD, CharacterRelationshipCRUD, RelationshipCRUD
from ..mappers import CharacterMapper
from ..schemas import CharacterCreate, CharacterUpdate, CharacterResponse, ResponseSchema, CharacterIdResponse, AdminCharacterResponse
from ..exceptions import NotFoundException, ForbiddenException


class CharacterService:
    def __init__(self, db: Session):
        self.db = db
        self.character_crud = CharacterCRUD(db)
        self.relationship_crud = RelationshipCRUD(db)
        self.character_relationship_crud = CharacterRelationshipCRUD(db)

    def _validate_relationship_ids(self, relationships: list) -> None:
        """
        캐릭터 관계 ID들의 유효성을 검증하는 내부 메서드
        Args:
            relationships (list): 검증할 관계 ID 목록
        Raises:
            NotFoundException: 존재하지 않는 관계 ID가 포함된 경우
        """
        # 모든 relationship ID 추출
        relationship_ids = [rel.relationship_id for rel in relationships]
        
        # 존재하는 relationship ID 조회
        existing_relationships = self.relationship_crud.get_relationships_by_ids(relationship_ids)
        existing_ids = {rel.relationship_id for rel in existing_relationships}
        
        # 존재하지 않는 ID 확인
        invalid_ids = set(relationship_ids) - existing_ids
        if invalid_ids:
            logger.warning(f"❌ Invalid relationship IDs found: {invalid_ids}")
            raise NotFoundException(
                "존재하지 않는 관계 ID가 포함되어 있습니다.",
                "relationship_ids",
                list(invalid_ids)
            )

    def create_character(self, character: CharacterCreate, user_id: int) -> ResponseSchema:
        """
        새로운 캐릭터 생성 서비스
        Args:
            character (CharacterCreate): 캐릭터 생성에 필요한 데이터
            user_id (int): 캐릭터를 생성하는 사용자 ID
        Returns:
            ResponseSchema: 생성 성공 메시지
        """
        try:
            # 트랜잭션 시작
            self.db.begin_nested()

            # 관계 ID 유효성 검증
            self._validate_relationship_ids(character.character_relationships)

            # 캐릭터 생성
            db_charater = self.character_crud.create(CharacterMapper.create_to_model(character, user_id))

            # 캐릭터 관계 생성
            unique_relationships = {rel.relationship_id: rel for rel in character.character_relationships}.values()

            for relationship in unique_relationships:
                self.character_relationship_crud.create(CharacterRelationship(character_id=db_charater.character_id, relationship_id=relationship.relationship_id))
        
            # 트랜잭션 커밋
            self.db.commit()
            
            logger.info(f"✨ Successfully created character: {db_charater.character_name} (ID: {db_charater.character_id})")
            return ResponseSchema(
                message="캐릭터가 성공적으로 생성되었습니다.",
                data=CharacterIdResponse(character_id=db_charater.character_id)
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Failed to create character: {str(e)}")
            raise
    
    def get_all_characters(self) -> list[CharacterResponse]:
        """
        모든 캐릭터 조회
        Returns:
            list[CharacterResponse]: 모든 캐릭터 목록
        """
        charaters = self.character_crud.get_charaters()
        logger.info(f"😊 Total {len(charaters)} public characters found")
        return CharacterMapper.to_dto_list(charaters)
    
    def get_character_by_id(self, character_id: int) -> AdminCharacterResponse:
        charater = self.character_crud.get_by_id(character_id)
        if not charater:
            logger.warning(f"❌ Failed to find character with id {character_id}")
            raise NotFoundException("캐릭터를 찾을 수 없습니다.", "character_id", character_id)
        
        logger.info(f"😊 Found character: {charater.character_name} (ID: {character_id})")
        return CharacterMapper.to_dto_for_admin(charater)
    
    def get_public_characters(self) -> list[CharacterResponse]:
        """
        공개된 모든 캐릭터 조회
        Returns:
            list[CharacterResponse]: 공개된 캐릭터 목록
        """
        charaters = self.character_crud.get_public_characters()
        logger.info(f"😊 Total {len(charaters)} public characters found")
        return CharacterMapper.to_dto_list(charaters)
    
    def get_top_used_public_characters(self, limit: int) -> list[CharacterResponse]:
        """
        가장 많이 사용된 공개 캐릭터 조회
        Args:
            limit (int): 조회할 캐릭터 수 (기본값: 5)
        Returns:
            list[CharacterResponse]: 상위 사용된 캐릭터 목록
        """
        charaters = self.character_crud.get_top_used_public_characters(limit)
        logger.info(f"😊 Found top {len(charaters)} most used public characters")
        return CharacterMapper.to_dto_list(charaters)
    
    def get_characters_by_user_id(self, user_id: int) -> list[CharacterResponse]:
        """
        특정 사용자의 모든 캐릭터 조회
        Args:
            user_id (int): 조회할 사용자 ID
        Returns:
            list[CharacterResponse]: 사용자의 캐릭터 목록
        """
        charaters = self.character_crud.get_characters_by_user_id(user_id)
        logger.info(f"😊 Found {len(charaters)} characters for user {user_id}")
        return CharacterMapper.to_dto_list(charaters)

    def get_public_character_by_id(self, character_id: int) -> CharacterResponse:
        """
        ID로 캐릭터 조회
        Args:
            character_id (int): 조회할 캐릭터 ID
        Returns:
            CharacterResponse: 조회된 캐릭터 정보
        Raises:
            NotFoundException: 캐릭터를 찾을 수 없는 경우
        """
        charater = self.character_crud.get_public_charater_by_id(character_id)
        if not charater:
            logger.warning(f"❌ Failed to find character with id {character_id}")
            raise NotFoundException("캐릭터를 찾을 수 없습니다.", "character_id", character_id)
        
        logger.info(f"😊 Found character: {charater.character_name} (ID: {character_id})")
        return CharacterMapper.to_dto(charater)

    def update_character(self, character_id: int, character :CharacterUpdate, user_id: int) -> ResponseSchema:
        """
        캐릭터 정보 업데이트
        Args:
            character_id (int): 업데이트할 캐릭터 ID
            character (CharacterUpdate): 업데이트할 캐릭터 정보
            user_id (int): 요청하는 사용자 ID
        Returns:
            ResponseSchema: 업데이트 성공 메시지
        Raises:
            NotFoundException: 캐릭터를 찾을 수 없는 경우
            ForbiddenException: 권한이 없는 경우
        """
        origin_character = self.character_crud.get_public_charater_by_id(character_id)
        if not origin_character:
            logger.warning(f"❌ Failed to find character with id {character_id}")
            raise NotFoundException("캐릭터를 찾을 수 없습니다.", "character_id", character_id)

        if user_id != origin_character.user_id:
            logger.warning(f"❌ User {user_id} attempted to modify character {character_id} owned by user {origin_character.user_id}")
            raise ForbiddenException("자신의 캐릭터만 수정할 수 있습니다.", "character_id", character_id)

        try:
            # 트랜잭션 시작
            self.db.begin_nested()

            # 관계 ID 유효성 검증
            self._validate_relationship_ids(character.character_relationships)

            # 기존 캐릭터 관계 삭제
            for cr in origin_character.character_relationships:
                self.character_relationship_crud.delete(cr.character_relationship_id)

            # 캐릭터 정보 업데이트
            db_charater = self.character_crud.update(character_id, CharacterMapper.create_to_model(character, user_id))

            # 캐릭터 관계 재생성
            unique_relationships = {rel.relationship_id: rel for rel in character.character_relationships}.values()

            for relationship in unique_relationships:
                self.character_relationship_crud.create(CharacterRelationship(character_id=db_charater.character_id, relationship_id=relationship.relationship_id))
        
            logger.info(f"🔄 Successfully updated character: {db_charater.character_name} (ID: {character_id})")
            return ResponseSchema(
                message="캐릭터가 성공적으로 수정되었습니다.",
                data=CharacterIdResponse(character_id=character_id)
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Failed to update character: {str(e)}")
            raise
    
    def deactive_charactor(self, character_id: int, user_id: int) -> ResponseSchema:
        """
        캐릭터 비활성화 (soft delete)
        Args:
            character_id (int): 비활성화할 캐릭터 ID
            user_id (int): 요청하는 사용자 ID
        Returns:
            ResponseSchema: 비활성화 성공 메시지
        Raises:
            NotFoundException: 캐릭터를 찾을 수 없는 경우
            ForbiddenException: 권한이 없는 경우
        """
        character = self.character_crud.get_public_charater_by_id(character_id)
        if not character:
            logger.warning(f"❌ Failed to find character with id {character_id}")
            raise NotFoundException("캐릭터를 찾을 수 없습니다.", "character_id", character_id)
        
        if user_id != character.user_id:
            logger.warning(f"❌ User {user_id} attempted to modify character {character_id} owned by user {character.user_id}")
            raise ForbiddenException("자신의 캐릭터만 비활성화할 수 있습니다.", "character_id", character_id)
        
        if self.character_crud.deactivate_character(character_id):
            logger.info(f"🚫 Successfully deactivated character: {character.character_name} (ID: {character_id})")
            return ResponseSchema(
                message="성공적으로 캐릭터를 비활성화 하였습니다.",
                data=CharacterIdResponse(character_id=character_id)
            )
    
    def delete_charactor(self, character_id: int, user_id: int) -> ResponseSchema:
        """
        캐릭터 완전 삭제
        Args:
            character_id (int): 삭제할 캐릭터 ID
            user_id (int): 요청하는 사용자 ID
        Returns:
            ResponseSchema: 삭제 성공 메시지
        Raises:
            NotFoundException: 캐릭터를 찾을 수 없는 경우
            ForbiddenException: 권한이 없는 경우
        """
        character = self.character_crud.get_charater_by_id(character_id)
        if not character:
            logger.warning(f"❌ Failed to find character with id {character_id}")
            raise NotFoundException("캐릭터를 찾을 수 없습니다.", "character_id", character_id)
        
        if user_id != character.user_id:
            logger.warning(f"❌ User {user_id} attempted to modify character {character_id} owned by user {character.user_id}")
            raise ForbiddenException("자신의 캐릭터만 삭제할 수 있습니다.", "character_id", character_id)
        
        if self.character_crud.delete(character_id):
            logger.info(f"🗑️  Successfully deleted character: {character.character_name} (ID: {character_id})")
            return ResponseSchema(
                message="캐릭터가 성공적으로 삭제되었습니다.",
                data=CharacterIdResponse(character_id=character_id)
            )
