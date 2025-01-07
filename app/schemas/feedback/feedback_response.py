from fastapi_camelcase import CamelModel
from datetime import datetime


class FeedbackResponse(CamelModel):
    feedback_id: int
    feedback_type: str
    feedback_title: str
    feedback_content: str
    feedback_image_url: str | None = None
    feedback_device_info: str
    feedback_app_version: str
    feedback_status: str
    feedback_create_at: datetime
    feedback_admin_comment: str | None = None
    feedback_resolved_at: datetime | None = None
    user_id: int
