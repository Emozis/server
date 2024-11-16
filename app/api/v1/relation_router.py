from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import AuthServiceDep
from app.schemas import LoginRequest, LoginGoogleRequest, ErrorResponse, LoginResponse


router = APIRouter(
    prefix="/api/v1/relationship",
    tags=["Relationship"]
)

@router.post(
    path="/",
    description="새 관계를 생성하는 API입니다."
)
@handle_exceptions
async def create_relationship():
    return

@router.get(
    path="/",
    description="모든 관계를 조회하는 API입니다."
)
@handle_exceptions
async def get_relationships():
    return

@router.put(
    path="/{relationship_id}",
    description="관계를 수정하는 API입니다."
)
@handle_exceptions
async def update_relationship():
    return

@router.delete(
    path="/{relationship_id}",
    description="관계를 삭제하는 API입니다.",
)
@handle_exceptions
async def delete_relationship():
    return