from sqlalchemy import Column, Integer, String, BigInteger, Text, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database.base import Base
from .enums import FeedbackType, FeedbackStatus


class Feedback(Base):
    __tablename__ = "feedbacks"

    feedback_id = Column(BigInteger, primary_key=True, autoincrement=True)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    feedback_title = Column(String(255), nullable=False)
    feedback_content = Column(Text, nullable=True)
    feedback_image_key = Column(String(500), nullable=True)
    feedback_device_info = Column(String(255), nullable=False)
    feedback_app_version = Column(String(255), nullable=False)
    feedback_status = Column(Enum(FeedbackStatus), nullable=False, default=FeedbackStatus.RECEIVED)
    feedback_create_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    feedback_admin_comment = Column(Text, nullable=True)
    feedback_resolved_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    user = relationship("User", back_populates="feedbacks")
