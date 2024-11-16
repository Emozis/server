from fastapi_camelcase import CamelModel


class RelationshipUpdate(CamelModel):
    relationship_name: str