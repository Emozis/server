from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core import get_current_user
from app.services import CharacterService
from app.schemas.request.character_request_schema import CharacterCreate, CharacterUpdate
from app.schemas.response.character_response_schema import CharacterResponse, CharacterCreateResponse, MessageResponse


router = APIRouter(
    prefix="/api/v1/characters",
    tags=["Characters"]
)

@router.post("/",
            description="새 캐릭터를 생성하는 API입니다.",
            response_model=CharacterCreateResponse
            )
async def create_character(character: CharacterCreate, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    character = CharacterService.create_character(character, user_id, db)
    return {"character_id": character.character_id, "message": "Character created successfully"}

@router.get("/",
            description="모든 캐릭터를 조회하는 API입니다.",
            response_model=list[CharacterResponse]
            )
async def get_all_characters(db: Session = Depends(get_db)):
    return CharacterService.get_all_characters(db)

@router.get("/{character_id}",
            description="특정 캐릭터를 조회하는 API입니다.",
            response_model=CharacterResponse
            )
async def get_character(character_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return CharacterService.get_character_by_character_id(character_id, user_id, db)

@router.get("/me/",
            description="인증된 사용자의 모든 캐릭터를 조회하는 API입니다.",
            response_model=list[CharacterResponse]
            )
async def get_my_characters(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return CharacterService.get_characters_by_user_id(user_id, db)

@router.get("/rank/",
            description="사용 횟수가 높은 상위 5개의 공개된 캐릭터를 조회하는 API입니다.",
            response_model=list[CharacterResponse]
            )
async def get_characters_by_rank(db: Session = Depends(get_db)):
    return CharacterService.get_characters_by_rank(7, db)

@router.put("/{character_id}",  
            description="특정 캐릭터 정보를 업데이트하는 API입니다.",
            response_model=MessageResponse
            )
async def update_character(character_id: int, character_update: CharacterUpdate, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    success = CharacterService.update_character_by_id(character_id, character_update, user_id, db)
    return {"message": "Character updated successfully"} if success else {"message": "Character update failed"}

@router.put("/{character_id}/deactivate",
            response_model=MessageResponse
            )
async def deactivate_character(character_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    deactivated_user = CharacterService.deactivate_character_by_id(character_id, user_id, db)
    return {"message": "Character deactivated successfully"} if deactivated_user else {"message": "Character deactivation failed"}

@router.delete("/{character_id}",
               description="특정 캐릭터를 삭제하는 API입니다.",
               response_model=MessageResponse
               )
async def delete_character(character_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    success = CharacterService.delete_character_by_id(character_id, user_id, db)
    return {"message": "Character deleted successfully"} if success else {"message": "Character deletion failed"}
