from pydantic import BaseModel


class JSONSchema(BaseModel):
    """Simple slug model."""

    id: str


class JSONSchemaDTO(BaseModel):
    """Simple slug model."""

    type: str
    json_schema: dict
