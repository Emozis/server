from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from ..db import db

class Relationship(db.Base):
    __tablename__ = "relationships"

    relationship_id = Column(BigInteger, primary_key=True, autoincrement=True)
    relationship_name = Column(String(255), nullable=False)

    character_relationships = relationship("CharacterRelationship", back_populates="relationship", cascade="all, delete-orphan")