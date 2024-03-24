import httpx
from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.json_schema import JSONSchemaDAO
from pipo_ai.db.dao.pipeline import PipelineDAO
from pipo_ai.services.code_sandbox import run_code
from pipo_ai.web.api.pipeline.schema import Code, Pipeline

router = APIRouter()


@router.post("/{id}", response_model=Pipeline)
async def create_pipeline(
    id: str,
    pipeline_dao: PipelineDAO = Depends(),
) -> Pipeline:
    """
    Create a pipeline with the given input.

    :param id: create a pipeline with the given id.
    :return: id of the created pipeline.
    """
    await pipeline_dao.create_pipeline_model(id=id)
    return Pipeline(id=str(id))


@router.post("/{id}/code", response_model=Pipeline)
async def update_pipeline_code(
    id: str,
    pipeline_input: Code,
    pipeline_dao: PipelineDAO = Depends(),
) -> Pipeline:
    """
    Update a pipeline with given input.

    :param code: input to update a pipeline.
    :return: id of the updated pipeline.
    """
    await pipeline_dao.upsert_pipeline_model(id=id, code=pipeline_input.code)
    return Pipeline(id=str(id))


@router.post("/{id}/start")
async def start_pipeline(
    id: str,
    pipeline_dao: PipelineDAO = Depends(),
) -> dict:
    """
    Start the pipeline.

    :param pipeline_input: input to update a pipeline.
    :return: id of the updated pipeline.
    """
    pipeline_with_schemas = await pipeline_dao.get_pipeline_model_with_schemas(
        id
    )
    if not pipeline_with_schemas:
        return {
            "error": f"Pipeline with id {id} not found.",
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
            "id": id,
        },
    )
    return {
        "message": "Pipeline started!",
    }


@router.post("/{id}/run")
async def run_pipeline(
    id: str,
    input_dict: dict,
    pipeline_dao: PipelineDAO = Depends(),
) -> dict:
    """
    Run the code of the pipeline.

    :param id: id of the pipeline.
    :param input_dict: Input data structure.
    :return: output of the pipeline.
    """
    pipeline = await pipeline_dao.get_pipeline_model(id)
    if not pipeline:
        return {
            "error": f"Pipeline with id {id} not found.",
        }
    output = run_code(pipeline.code, input_dict)

    return output


@router.post("/{id}/json_schema/input")
async def upsert_input_json_schema(
    id: str,
    schema: dict,
    pipeline_dao: PipelineDAO = Depends(),
    json_schema_dao: JSONSchemaDAO = Depends(),
) -> dict:
    """
    Update the input JSON schema for a pipeline.

    :param id: id of the pipeline.
    :return: updated JSON schema.
    """
    pipeline = await pipeline_dao.get_pipeline_model(id)
    if not pipeline:
        return {
            "error": f"Pipeline with id {id} not found.",
        }

    await json_schema_dao.upsert_json_schema_model(
        schema=schema, type="input", pipeline_id=pipeline.id
    )
    return {"message": "Success!"}


@router.post("/{id}/json_schema/output")
async def upsert_output_json_schema(
    id: str,
    schema: dict,
    pipeline_dao: PipelineDAO = Depends(),
    json_schema_dao: JSONSchemaDAO = Depends(),
) -> dict:
    """
    Update the output JSON schema for a pipeline.

    :param id: id of the pipeline.
    :return: updated JSON schema.
    """
    pipeline = await pipeline_dao.get_pipeline_model(id)
    if not pipeline:
        return {
            "error": f"Pipeline with id {id} not found.",
        }

    await json_schema_dao.upsert_json_schema_model(
        schema=schema, type="output", pipeline_id=pipeline.id
    )
    return {"message": "Success!"}
