from sqlalchemy.orm import Session, joinedload

from ..models import Character, CharacterRelationship
from .base_crud import BaseCRUD


class CharacterCRUD(BaseCRUD[Character]):
    """
    캐릭터 관련 CRUD 작업을 처리하는 클래스입니다.
    Character 모델에 대한 데이터베이스 조작을 담당합니다.
    """

    def __init__(self, db: Session):
        super().__init__(model=Character, db=db, id_field='character_id')

    def get_charaters(self) -> list[Character]:
        """
        모든 캐릭터 정보를 조회합니다.
        관련된 사용자 정보와 캐릭터 관계 정보를 함께 로드합니다.
        
        Returns:
            list[Character]: 모든 캐릭터 목록
        """
        return self.db.query(Character)\
            .options(
                joinedload(Character.user), 
                joinedload(Character.character_relationships)\
                    .joinedload(CharacterRelationship.relationship)
            )\
            .all()

    def get_public_characters(self) -> list[Character]:
        """
        공개된(character_is_public=True) 캐릭터만 조회합니다.
        
        Returns:
            list[Character]: 공개된 캐릭터 목록
        """
        return self.db.query(Character)\
            .options(
                joinedload(Character.user),
                joinedload(Character.character_relationships)\
                    .joinedload(CharacterRelationship.relationship)
            )\
            .filter(Character.character_is_public == True)\
            .filter(Character.character_is_active == True)\
            .all()
    
    def get_top_used_public_characters(self, limit: int = 5) -> list[Character]:
        """
        공개된 캐릭터 중 사용 횟수(character_usage_count)가 가장 높은 n개의 캐릭터를 조회합니다.
        
        Args:
            limit (int): 조회할 캐릭터의 수. 기본값은 10개
            
        Returns:
            list[Character]: 사용량 상위 n개의 공개 캐릭터 목록
        """
        return self.db.query(Character)\
            .options(
                joinedload(Character.user),
                joinedload(Character.character_relationships)\
                    .joinedload(CharacterRelationship.relationship)
            )\
            .filter(Character.character_is_public == True)\
            .filter(Character.character_is_active == True)\
            .order_by(Character.character_usage_count.desc())\
            .limit(limit)\
            .all()

    def get_characters_by_user_id(self, user_id: int) -> list[Character]:
        """
        특정 user_id에 해당하는 모든 캐릭터를 조회합니다.
        
        Args:
            user_id (int): 조회할 사용자의 ID
            
        Returns:
            list[Character]: 해당 사용자의 모든 캐릭터 목록
        """
        return self.db.query(Character)\
            .options(
                joinedload(Character.user),
                joinedload(Character.character_relationships)\
                    .joinedload(CharacterRelationship.relationship)
            )\
            .filter(Character.user_id == user_id)\
            .filter(Character.character_is_active == True)\
            .all()
    
    def get_public_charater_by_id(self, character_id: int) -> Character:
        return self.db.query(Character)\
            .options(
                joinedload(Character.user), 
                joinedload(Character.character_relationships)\
                    .joinedload(CharacterRelationship.relationship)
            )\
            .filter(Character.character_id == character_id)\
            .filter(Character.character_is_active == True)\
            .first()
    
    def get_charater_by_id(self, character_id: int) -> Character:
        return self.db.query(Character)\
            .options(
                joinedload(Character.user), 
                joinedload(Character.character_relationships)\
                    .joinedload(CharacterRelationship.relationship)
            )\
            .filter(Character.character_id == character_id)\
            .first()
    
    def deactivate_character(self, character_id: int) -> bool:
        """
        특정 캐릭터를 비활성화합니다. 
        character_is_active를 False로 설정하고 character_is_public도 False로 설정합니다.
        
        Args:
            character_id (int): 비활성화할 캐릭터의 ID
            
        Returns:
            bool: 비활성화 성공 여부. 캐릭터가 존재하지 않으면 False를 반환합니다.
        """
        character = self.db.query(Character)\
            .filter(Character.character_id == character_id)\
            .first()
        
        if not character:
            return False
        
        character.character_is_active = False
        character.character_is_public = False  # 비활성화 시 공개 상태도 False로 변경
        
        try:
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False