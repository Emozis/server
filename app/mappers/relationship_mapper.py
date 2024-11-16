from ..models import Relationship
from ..schemas import RelationshipCreate, RelationshipUpdate, RelationshipResponse

class RelationshipMapper:
    @staticmethod
    def create_to_model(dto: RelationshipCreate) -> Relationship:
        return Relationship(
            relationship_name=dto.relationship_name
        )
    
    @staticmethod
    def update_to_model(dto: RelationshipUpdate) -> Relationship:
        return Relationship(
            relationship_name=dto.relationship_name
        )
    
    @staticmethod
    def to_dto(model: Relationship) -> RelationshipResponse:
        return RelationshipResponse(
            relationship_id=model.relationship_id,
            relationship_name=model.relationship_name
        )
    
    @staticmethod
    def to_dto_list(models: list[Relationship]) -> list[RelationshipResponse]:
        return [RelationshipMapper.to_dto(model) for model in models]