from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.json_schema import JSONSchemaDAO
from pipo_ai.db.dao.pipeline import PipelineDAO
from pipo_ai.services.code_sandbox import run_code
from pipo_ai.web.api.pipeline.schema import Pipeline, Slug

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


@router.post("/{slug}")
async def run_pipeline(
    slug: str,
    input_dict: dict,
    pipeline_dao: PipelineDAO = Depends(),
) -> dict:
    """
    Run the pipeline.

    :param slug: slug of the pipeline.
    :param input_dict: Input data structure.
    :return: output of the pipeline.
    """
    pipeline = await pipeline_dao.get_pipeline_model(slug)
    if not pipeline:
        return {
            "error": f"Pipeline with slug {slug} not found.",
        }
    output = run_code(pipeline.code, input_dict)

    return output


@router.post("/{slug}/json_schema/input")
async def upsert_input_json_schema(
    slug: str,
    schema: dict,
    pipeline_dao: PipelineDAO = Depends(),
    json_schema_dao: JSONSchemaDAO = Depends(),
) -> dict:
    """
    Update the input JSON schema for a pipeline.

    :param slug: slug of the pipeline.
    :return: updated JSON schema.
    """
    pipeline = await pipeline_dao.get_pipeline_model(slug)
    if not pipeline:
        return {
            "error": f"Pipeline with slug {slug} not found.",
        }

    json_schema_dao.upsert_json_schema_model(schema=schema, slug=slug)
    return {"message": "Success!"}


@router.post("/{slug}/json_schema/output")
async def upsert_output_json_schema(
    slug: str,
    schema: dict,
    pipeline_dao: PipelineDAO = Depends(),
    json_schema_dao: JSONSchemaDAO = Depends(),
) -> dict:
    """
    Update the output JSON schema for a pipeline.

    :param slug: slug of the pipeline.
    :return: updated JSON schema.
    """
    pipeline = await pipeline_dao.get_pipeline_model(slug)
    if not pipeline:
        return {
            "error": f"Pipeline with slug {slug} not found.",
        }

    json_schema_dao.upsert_json_schema_model(schema=schema, slug=slug)
    return {"message": "Success!"}
