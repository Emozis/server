from sqlalchemy import Column, BigInteger, String, Enum, DateTime
from datetime import datetime

from ..database.base import Base
from .enums import ImageAgeGroupEnum, ImageGenderEnum

class DefaultImages(Base):
    __tablename__ = "default_images"

    image_id = Column(BigInteger, primary_key=True, autoincrement=True)
    image_name = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=False)
    image_gender = Column(Enum(ImageGenderEnum), nullable=True)
    image_age_group = Column(Enum(ImageAgeGroupEnum), nullable=True)
    image_emotion = Column(String(255), nullable=True)

    image_created_at = Column(DateTime, default=datetime.now)
    image_updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)