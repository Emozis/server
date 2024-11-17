from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import RelationshipServiceDep
from app.schemas import RelationshipCreate, RelationshipUpdate, RelationshipResponse, ErrorResponse, MessageResponse


router = APIRouter(
    prefix="/api/v1/default-images",
    tags=["Default image"]
)

@router.post(
    path="/",
    description="기본 이미지을 저장하는 API입니다.",
)
@handle_exceptions
async def create_default_image():
    return 

@router.get(
    path="/",
    description="기본 이미지를 불러오는 API입니다.",
)
@handle_exceptions
async def get_default_images():
    return 
