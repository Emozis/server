from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import RelationshipServiceDep
from app.schemas import (
    RelationshipCreate, 
    RelationshipUpdate, 
    RelationshipResponse, 
    ErrorResponse, 
    ResponseSchema, 
    ResponseSchema, 
    RelationshipIdResponse
)


router = APIRouter(
    prefix="/api/v1/relationship",
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
async def create_relationship(relationship: RelationshipCreate, relationship_service: RelationshipServiceDep) -> ResponseSchema:
    return relationship_service.create_relationship(relationship)

@router.get(
    path="",
    description="모든 관계를 조회하는 API입니다.",
    responses={
        200: {"model": list[RelationshipResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def get_relationships(relationship_service: RelationshipServiceDep) -> list[RelationshipResponse]:
    return relationship_service.get_relationships()

@router.get(
    path="/{relationship_id}",
    description="관계를 조회하는 API입니다.",
    responses={
        200: {"model": RelationshipResponse, "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@handle_exceptions
async def get_relationship(relationship_id: int, relationship_service: RelationshipServiceDep) -> RelationshipResponse:
    return relationship_service.get_relationship_by_id(relationship_id)

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
async def update_relationship(relationship_id: int, relationship: RelationshipUpdate, relationship_service: RelationshipServiceDep) -> ResponseSchema:
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
async def delete_relationship(relationship_id: int, relationship_service: RelationshipServiceDep):
    return relationship_service.delete_relationship(relationship_id)