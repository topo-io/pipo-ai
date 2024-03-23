from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.pipeline import PipelineDAO
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
    return pipeline_input.slug


@router.post("/{slug}", response_model=Message)
async def send_echo_message(
    slug: str,
    incoming_message: Message,
) -> Message:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """
    return incoming_message
