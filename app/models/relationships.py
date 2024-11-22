from sqlalchemy import Column, String, BigInteger, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database.base import Base


class Relationship(Base):
    __tablename__ = "relationships"

    relationship_id = Column(BigInteger, primary_key=True, autoincrement=True)
    relationship_name = Column(String(255), nullable=False)
    relationship_created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    character_relationships = relationship("CharacterRelationship", back_populates="relationship", cascade="all, delete-orphan")