from pydantic import BaseModel


class JSONSchemaSlug(BaseModel):
    """Simple slug model."""

    slug: str
