from ..models import Feedback
from ..schemas import FeedbackCreate, FeedbackResponse
from ..utils.aws_manager import aws_managers


class FeedbackMapper:
    @staticmethod
    def create_to_model(dto: FeedbackCreate, user_id: int) -> Feedback:
        return Feedback(
            feedback_type=dto.feedback_type,
            feedback_title=dto.feedback_title,
            feedback_content=dto.feedback_content,
            feedback_image_key=dto.feedback_image_key,
            feedback_device_info=dto.feedback_device_info,
            feedback_app_version=dto.feedback_app_version,
            user_id=user_id
        )

    @staticmethod
    def to_dto(model: Feedback) -> FeedbackResponse:
        return FeedbackResponse(
            feedback_id=model.feedback_id,
            feedback_type=model.feedback_type,
            feedback_title=model.feedback_title,
            feedback_content=model.feedback_content,
            feedback_image_url=aws_managers.get_cloudfront_url(model.feedback_image_key) if model.feedback_image_key else None,
            feedback_device_info=model.feedback_device_info,
            feedback_app_version=model.feedback_app_version,
            feedback_status=model.feedback_status,
            feedback_create_at=model.feedback_create_at,
            feedback_admin_comment=model.feedback_admin_comment,
            feedback_resolved_at=model.feedback_resolved_at,
            user_id=model.user_id
        )
    
    @staticmethod
    def to_dto_list(models: list[Feedback]) -> list[FeedbackResponse]:
        return [FeedbackMapper.to_dto(model) for model in models]