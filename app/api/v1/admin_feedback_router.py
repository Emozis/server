from fastapi import APIRouter

from app.core import handle_exceptions
from app.core.dependencies import AdminUser, FeedbackServiceDep
from app.schemas import (
    FeedbackResponse, 
    FeedbackIdResponse,
    FeedbackReplyRequest,
    ResponseSchema,
    ErrorResponse, 
)


router = APIRouter(
    prefix="/api/v1/admin/feedback",
    tags=["Feedback"]
)

@router.get(
    path="",
    description="유저 피드백을 전부를 불러오는 API입니다.",
    responses={
        200: {"model": list[FeedbackResponse], "description": "Successful Response"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_feedbacks(feedback_service: FeedbackServiceDep, admin_id: AdminUser) -> list[FeedbackResponse]:
    return feedback_service.get_feedbacks()

@router.get(
    path="/{feedback_id}",
    description="유저 피드백을 불러오는 API입니다.",
    responses={
        200: {"model": FeedbackResponse, "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def get_image(feedback_id: int, feedback_service: FeedbackServiceDep, admin_id: AdminUser) -> FeedbackResponse:
    return feedback_service.get_feedback_by_id(feedback_id)

@router.delete(
    path="/{feedback_id}",
    description="유저 피드백을 삭제하는 API입니다.",
    responses={
        200: {"model": ResponseSchema[FeedbackIdResponse], "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def delete_image(feedback_id: int, feedback_service: FeedbackServiceDep, admin_id: AdminUser) -> ResponseSchema:
    return feedback_service.delete_feedback(feedback_id)

@router.patch(
    path="/{feedback_id}/reply",
    description="관리자가 유저 피드백에 답변을 보내는 API입니다.",
    responses={
        200: {"model": ResponseSchema[FeedbackIdResponse], "description": "Successful Response"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
@handle_exceptions
async def update_feedback_comment(
    feedback_id: int, 
    reply: FeedbackReplyRequest, 
    feedback_service: FeedbackServiceDep, 
    admin_id: AdminUser
) -> ResponseSchema:
    return feedback_service.update_feedback_comment(feedback_id, reply)