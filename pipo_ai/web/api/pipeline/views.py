import httpx
from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.json_schema import JSONSchemaDAO
from pipo_ai.db.dao.pipeline import PipelineDAO
from pipo_ai.services.code_sandbox import run_code
from pipo_ai.web.api.pipeline.schema import Code, PipelineSlug

router = APIRouter()


@router.post("/{slug}", response_model=PipelineSlug)
async def create_pipeline(
    slug: str,
    pipeline_dao: PipelineDAO = Depends(),
) -> PipelineSlug:
    """
    Create a pipeline with the given input.

    :param slug: create a pipeline with the given slug.
    :return: slug of the created pipeline.
    """
    await pipeline_dao.create_pipeline_model(slug=slug)
    return PipelineSlug(slug=slug)


@router.post("/{slug}/code", response_model=PipelineSlug)
async def update_pipeline_code(
    slug: str,
    pipeline_input: Code,
    pipeline_dao: PipelineDAO = Depends(),
) -> PipelineSlug:
    """
    Update a pipeline with given input.

    :param code: input to update a pipeline.
    :return: slug of the updated pipeline.
    """
    await pipeline_dao.upsert_pipeline_model(
        slug=slug, code=pipeline_input.code
    )
    return PipelineSlug(slug=slug)


@router.post("/{slug}/start")
async def start_pipeline(
    slug: str,
    pipeline_dao: PipelineDAO = Depends(),
) -> dict:
    """
    Start the pipeline.

    :param pipeline_input: input to update a pipeline.
    :return: slug of the updated pipeline.
    """
    pipeline_with_schemas = await pipeline_dao.get_pipeline_model_with_schemas(
        slug
    )
    if not pipeline_with_schemas:
        return {
            "error": f"Pipeline with slug {slug} not found.",
        }

    input_format = next(
        (
            schema
            for schema in pipeline_with_schemas.json_schemas
            if schema.type == "input"
        ),
        None,
    )

    output_format = next(
        (
            schema
            for schema in pipeline_with_schemas.json_schemas
            if schema.type == "output"
        ),
        None,
    )

    if not input_format or not output_format:
        return {
            "error": "Input and output schemas are required.",
        }

    httpx.post(
        "https://automation.topo.io/webhook/11136b88-f235-4597-b9f6-48b3959c2388",
        data={
            "input_format": input_format.value,
            "output_format": output_format.value,
            "slug": slug,
        },
    )
    return {
        "message": "Pipeline started!",
    }


@router.post("/{slug}/run")
async def run_pipeline(
    slug: str,
    input_dict: dict,
    pipeline_dao: PipelineDAO = Depends(),
) -> dict:
    """
    Run the code of the pipeline.

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

    await json_schema_dao.upsert_json_schema_model(
        schema=schema, type="input", pipeline_id=pipeline.id
    )
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

    await json_schema_dao.upsert_json_schema_model(
        schema=schema, type="output", pipeline_id=pipeline.id
    )
    return {"message": "Success!"}
