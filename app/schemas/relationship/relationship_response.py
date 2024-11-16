from fastapi_camelcase import CamelModel

class RelationshipResponse(CamelModel):
    relationship_id: int
    relationship_name: str