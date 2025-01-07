from fastapi import APIRouter
from fastapi import Form, File, UploadFile
from pydantic import ValidationError

from app.core import handle_exceptions
from app.core.dependencies import FeedbackServiceDep, AuthenticatedUser
from app.schemas import (
    FeedbackCreate, 
    ErrorResponse, 
    ResponseSchema, 
    FeedbackIdResponse
)
from app.exceptions.default_image_exception import (
    UnsupportedImageFormatException,
    InvalidEnumValueException
)


router = APIRouter(
    prefix="/api/v1/feedback",
    tags=["Feedback"]
)

@router.post(
    path="",
    description="유저 피드백을 등록하는 API입니다.",
    responses={
        200: {"model": ResponseSchema[FeedbackIdResponse], "description": "Successful Response"},
        415: {"model": ErrorResponse, "description": "Unsupported Media Type"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def create_feedback(
    user_id: AuthenticatedUser,
    feedback_service: FeedbackServiceDep,
    feedback_type: str = Form(...), 
    feedback_title: str = Form(...), 
    feedback_content: str = Form(...),
    feedback_device_info: str = Form(...), 
    feedback_app_version: str = Form(...),
    image: UploadFile = File(None)
) -> ResponseSchema:
    if image and not image.content_type.startswith('image/'):
        raise UnsupportedImageFormatException(content_type=image.content_type)

    try:
        feedback = FeedbackCreate(
            feedback_type=feedback_type,
            feedback_title=feedback_title,
            feedback_content=feedback_content,
            feedback_device_info=feedback_device_info,
            feedback_app_version=feedback_app_version
        )
    except ValidationError as e:
        enum_error = InvalidEnumValueException.from_validation_error(e)
        if enum_error is not None:
            raise enum_error
        raise

    return await feedback_service.create_feedback(feedback, image, user_id)

# @router.put(
#     path="/{image_id}",
#     description="기본 이미지를 수정하는 API입니다.",
#     responses={
#         200: {"model": ResponseSchema[DefaultImageIdResponse], "description": "Successful Response"},
#         400: {"model": ErrorResponse, "description": "Bad Request"},
#         404: {"model": ErrorResponse, "description": "Not Found"},
#         415: {"model": ErrorResponse, "description": "Unsupported Media Type"},
#         500: {"model": ErrorResponse, "description": "Internal Server Error"}
#     }
# )
# @handle_exceptions
# async def update_image(
#     image_id: int,
#     admin_id: AdminUser,
#     default_image_service: DefaultImageServiceDep,
#     gender: str = Form(...), 
#     ageGroup: str = Form(...), 
#     emotion: str = Form(...), 
#     image: UploadFile = File(...)
# ) -> ResponseSchema:
#     if not image.content_type.startswith('image/'):
#         raise UnsupportedImageFormatException(content_type=image.content_type)
    
#     try:
#         default_image = DefaultImageCreate(
#             image_gender=gender,
#             image_age_group=ageGroup,
#             image_emotion=emotion
#         )
#     except ValidationError as e:
#         enum_error = InvalidEnumValueException.from_validation_error(e)
#         if enum_error is not None:
#             raise enum_error
#         raise
    
#     return await default_image_service.update_default_image(image_id, default_image, image)

# @router.delete(
#     path="/{image_id}",
#     description="기본 이미지를 삭제하는 API입니다.",
#     responses={
#         200: {"model": ResponseSchema[DefaultImageIdResponse], "description": "Successful Response"},
#         404: {"model": ErrorResponse, "description": "Not Found"},
#         500: {"model": ErrorResponse, "description": "Internal Server Error"}
#     }
# )
# @handle_exceptions
# async def delete_image(image_id: int, admin_id: AdminUser, default_image_service: DefaultImageServiceDep) -> ResponseSchema:
#     return default_image_service.delete_default_image(image_id)
