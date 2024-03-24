from pydantic import BaseModel


class Message(BaseModel):
    """Simple message model."""

    message: str


class Slug(BaseModel):
    """Simple slug model."""

    slug: str


class Code(BaseModel):
    """Simple code model."""

    code: str


class Pipeline(BaseModel):
    """Simple pipeline model."""

    code: str
