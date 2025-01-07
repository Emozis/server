from sqlalchemy.orm import Session
from fastapi import UploadFile

from ..core import logger
from ..models import Feedback
from ..crud import FeedbackCRUD
from ..mappers import FeedbackMapper
from ..schemas import ResponseSchema, FeedbackCreate, FeedbackResponse, FeedbackIdResponse, FeedbackReplyRequest
from ..exceptions import NotFoundException
from ..utils.aws_manager import aws_managers


class FeedbackService:
    def __init__(self, db: Session):
        self.db = db
        self.feedback_crud = FeedbackCRUD(db)

    def _get_feedback_or_raise(self, feedback_id: int) -> Feedback:
        feedback = self.feedback_crud.get_by_id(feedback_id)
        if not feedback:
            logger.warning(f"❌ Failed to find feedback with id {feedback_id}")
            raise NotFoundException("피드백을 찾을 수 없습니다.", "feedback_id", feedback_id)
        return feedback

    async def create_feedback(self, feedback: FeedbackCreate, image: UploadFile, user_id: int) -> ResponseSchema:
        # S3에 이미지 업로드
        if image:
            feedback.feedback_image_key = await aws_managers.upload_to_s3(file=image, folder_path="feedback")

        created = self.feedback_crud.create(FeedbackMapper.create_to_model(feedback, user_id))
        logger.info(f"✨ Successfully created feedback: {created.feedback_title} (ID: {created.feedback_id})")
        return ResponseSchema(
            message="피드백이 성공적으로 생성되었습니다.",
            data=FeedbackIdResponse(feedback_id=created.feedback_id)
        )

    def get_feedbacks(self) -> list[FeedbackResponse]:
        feedbacks = self.feedback_crud.get_all()
        logger.info(f"🤝 Total {len(feedbacks)} feedbacks found")
        return FeedbackMapper.to_dto_list(feedbacks)
    
    def get_feedback_by_id(self, feedback_id: int) -> FeedbackResponse:
        feedback = self._get_feedback_or_raise(feedback_id)
        logger.info(f"🤝 Found feedback: {feedback.feedback_title} (ID: {feedback_id})")
        return FeedbackMapper.to_dto(feedback)
    
    def update_feedback_comment(self, feedback_id: int, reply: FeedbackReplyRequest) -> ResponseSchema:
        feedback = self._get_feedback_or_raise(feedback_id)
        feedback.feedback_admin_comment = reply.feedback_admin_comment
        self.feedback_crud.update(feedback_id, feedback)
        
        logger.info(f"✏️  Successfully updated feedback comment for: {feedback.feedback_title} (ID: {feedback_id})")
        return ResponseSchema(
            message="피드백 답변이 성공적으로 등록되었습니다.",
            data=FeedbackIdResponse(feedback_id=feedback_id)
        )

    def delete_feedback(self, feedback_id: int) -> ResponseSchema:
        feedback = self._get_feedback_or_raise(feedback_id)
        if self.feedback_crud.delete(feedback_id):
            logger.info(f"🗑️  Successfully deleted feedback: {feedback.feedback_title} (ID: {feedback_id})")
            return ResponseSchema(
                message="피드백이 성공적으로 삭제되었습니다.",
                data=FeedbackIdResponse(feedback_id=feedback_id)
            )