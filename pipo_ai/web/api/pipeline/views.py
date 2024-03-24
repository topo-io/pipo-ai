from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.pipeline import PipelineDAO
from pipo_ai.services.code_sandbox import run_code
from pipo_ai.web.api.pipeline.schema import Message, Pipeline, Slug

router = APIRouter()


@router.post("/", response_model=Slug)
async def create_pipeline(
    pipeline_input: Pipeline,
    pipeline_dao: PipelineDAO = Depends(),
) -> str:
    """
    Create a pipeline with the given input.

    :param incoming_message: incoming message.
    :return: message same as the incoming.
    """
    await pipeline_dao.create_pipeline_model(
        code=pipeline_input.code, slug=pipeline_input.slug
    )
    return Slug(slug=pipeline_input.slug)


@router.post("/{slug}", response_model=Message)
async def run_pipeline(
    slug: str,
    incoming_message: Message,
    pipeline_dao: PipelineDAO = Depends(),
) -> Message:
    """
    Run the pipeline.

    :param slug: slug of the pipeline.
    :return: output of the pipeline.
    """
    pipeline = await pipeline_dao.get_pipeline_model(slug)
    if not pipeline:
        return Message(message="Pipeline not found")
    output = run_code(pipeline.code, {"value": incoming_message.message})

    return Message(message=f"{output}")
