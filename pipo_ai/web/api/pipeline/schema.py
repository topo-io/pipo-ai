from pydantic import BaseModel


class Message(BaseModel):
    """Simple message model."""

    message: str


class Pipeline(BaseModel):
    """Simple model."""

    id: str


class PipelineInput(BaseModel):
    """Simple pipeline input model."""

    input_schema_id: str
    output_schema_id: str


class Code(BaseModel):
    """Simple code model."""

    code: str
