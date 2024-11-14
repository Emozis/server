from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.user_service import UserService

router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

@router.get("/")
async def read_users(db: Session = Depends(get_db)):
    """새로운 유저 생성 엔드포인트"""
    try:
        user_service = UserService(db)
        user = user_service.create_user()
        return user
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )