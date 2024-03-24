from pydantic import BaseModel


class JSONSchema(BaseModel):
    """Simple slug model."""

    id: str
