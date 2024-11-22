from sqlalchemy import Column, BigInteger, String, Enum, TIMESTAMP
from sqlalchemy.sql import func

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

    image_created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    image_updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()) 