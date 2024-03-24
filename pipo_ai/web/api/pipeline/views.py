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
) -> Slug:
    """
    Create a pipeline with the given input.

    :param pipeline_input: input for creating the pipeline.
    :return: slug of the created pipeline.
    """
    await pipeline_dao.create_pipeline_model(
        code=pipeline_input.code, slug=pipeline_input.slug
    )
    return Slug(slug=pipeline_input.slug)


@router.post("/{slug}", response_model=Message)
async def run_pipeline(
    slug: str,
    input_dict: Message,
    pipeline_dao: PipelineDAO = Depends(),
) -> Message:
    """
    Run the pipeline.

    :param slug: slug of the pipeline.
    :param input_dict: Input data structure.
    :return: output of the pipeline.
    """
    pipeline = await pipeline_dao.get_pipeline_model(slug)
    if not pipeline:
        return Message(message="Pipeline not found")
    output = run_code(pipeline.code, {"value": input_dict.message})

    return Message(message=f"{output}")
