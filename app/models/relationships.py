from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base

class Relationship(Base):
    __tablename__ = "relationships"

    relationship_id = Column(Integer, primary_key=True, autoincrement=True)
    relationship_name = Column(String(255), nullable=False)

    character_relationships = relationship("CharacterRelationship", back_populates="relationship", cascade="all, delete-orphan")