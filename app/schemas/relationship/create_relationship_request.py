from fastapi_camelcase import CamelModel


class RelationshipCreate(CamelModel):
    relationship_name: str