from fastapi_camelcase import CamelModel

from ...models.enums import FeedbackType


class FeedbackCreate(CamelModel):
    feedback_type: FeedbackType
    feedback_title: str
    feedback_content: str
    feedback_image_key: str | None = None
    feedback_device_info: str
    feedback_app_version: str