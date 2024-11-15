from fastapi import APIRouter

from app.core import handle_exceptions, UserServiceDep
from app.schemas import UserCreate, UserUpdate, UserResponse, ErrorResponse, MessageResponse


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

@router.post(
    path="/login/google/id-token",
    description="구글 로그인시 발급되는 id-token을 사용하여 인증합니다."
    )
async def auth_google_token(data: auth_request_schema.LoginGoogleIdToken, db: Session = Depends(get_db)):
    response = AuthService.auth_google_id_token(data.id_token, db)
    logger.info(f"📌 return access token - {response['access_token']}")

    return response