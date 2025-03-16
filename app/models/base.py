from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func

from ..database.base import Base


class TimeStampedModel(Base):
    __abstract__ = True

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) 