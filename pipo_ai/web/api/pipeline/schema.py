from pydantic import BaseModel


class Message(BaseModel):
    """Simple message model."""

    message: str


class Pipeline(BaseModel):
    """Simple model."""

    id: str


class Code(BaseModel):
    """Simple code model."""

    code: str
