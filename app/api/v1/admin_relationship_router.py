from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import RelationshipServiceDep, AdminUser
from app.schemas import (
    RelationshipCreate, 
    RelationshipUpdate, 
    ErrorResponse, 
    ResponseSchema, 
    RelationshipIdResponse
)


router = APIRouter(
    prefix="/api/v1/admin/relationship",
    tags=["Relationship"]
)

@router.post(
    path="",
    description="새 관계를 생성하는 API입니다.",
    responses={
        200: {"model": ResponseSchema[RelationshipIdResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def create_relationship(relationship: RelationshipCreate, admin_id: AdminUser, relationship_service: RelationshipServiceDep) -> ResponseSchema:
    return relationship_service.create_relationship(relationship)

@router.put(
    path="/{relationship_id}",
    description="관계를 수정하는 API입니다.",
        responses={
        200: {"model": ResponseSchema[RelationshipIdResponse], "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def update_relationship(relationship_id: int, relationship: RelationshipUpdate, admin_id: AdminUser, relationship_service: RelationshipServiceDep) -> ResponseSchema:
    return relationship_service.update_relationship(relationship_id, relationship)

@router.delete(
    path="/{relationship_id}",
    description="관계를 삭제하는 API입니다.",
    responses={
        200: {"model": ResponseSchema[RelationshipIdResponse], "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def delete_relationship(relationship_id: int, admin_id: AdminUser, relationship_service: RelationshipServiceDep):
    return relationship_service.delete_relationship(relationship_id)