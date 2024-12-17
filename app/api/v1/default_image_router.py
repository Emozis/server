from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import DefaultImageServiceDep
from app.schemas import (
    DefaultImageResponse, 
    ErrorResponse, 
)


router = APIRouter(
    prefix="/api/v1/default-image",
    tags=["Default image"]
)

@router.get(
    path="",
    description="기본 이미지 전부를 불러오는 API입니다.",
    responses={
        200: {"model": list[DefaultImageResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_images(default_image_service: DefaultImageServiceDep) -> list[DefaultImageResponse]:
    return default_image_service.get_default_images()

@router.get(
    path="/{image_id}",
    description="기본 이미지를 불러오는 API입니다.",
    responses={
        200: {"model": DefaultImageResponse, "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_image(image_id: int, default_image_service: DefaultImageServiceDep) -> DefaultImageResponse:
    return default_image_service.get_default_image(image_id)
