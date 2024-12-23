from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import RelationshipServiceDep
from app.schemas import (
    RelationshipCreate, 
    RelationshipUpdate, 
    RelationshipResponse, 
    ErrorResponse, 
    ResponseSchema, 
    RelationshipIdResponse
)


router = APIRouter(
    prefix="/api/v1/relationship",
    tags=["Relationship"]
)

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
