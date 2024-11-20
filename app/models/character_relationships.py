from sqlalchemy import Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from ..database.base import Base


class CharacterRelationship(Base):
    __tablename__ = "character_relationships"

    character_relationship_id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_id = Column(BigInteger, ForeignKey('characters.character_id'), nullable=False)
    relationship_id = Column(BigInteger, ForeignKey('relationships.relationship_id'), nullable=False)

    character = relationship("Character", back_populates="character_relationships")
    relationship = relationship("Relationship")