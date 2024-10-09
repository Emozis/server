from sqlalchemy import Column, BigInteger, String, Enum

from ..db import db
from .enums import ImageAgeGroupEnum, ImageGenderEnum

class DefaultImages(db.Base):
    __tablename__ = "default_images"

    image_id = Column(BigInteger, primary_key=True, autoincrement=True)
    image_name = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=False)
    image_gender = Column(Enum(ImageGenderEnum), nullable=True)
    image_age_group = Column(Enum(ImageAgeGroupEnum), nullable=True)