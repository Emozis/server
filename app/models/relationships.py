from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database.base import Base


class Relationship(Base):
    __tablename__ = "relationships"

    relationship_id = Column(BigInteger, primary_key=True, autoincrement=True)
    relationship_name = Column(String(255), nullable=False)
    relationship_created_at = Column(DateTime, default=datetime.now)

    character_relationships = relationship("CharacterRelationship", back_populates="relationship", cascade="all, delete-orphan")