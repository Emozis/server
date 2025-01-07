from fastapi_camelcase import CamelModel


class FeedbackReplyRequest(CamelModel):
    feedback_admin_comment: str