import httpx
from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.pipeline import PipelineDAO
from pipo_ai.services.code_sandbox import run_code
from pipo_ai.web.api.pipeline.schema import Code, Pipeline, PipelineInput

router = APIRouter()


@router.post("/")
async def create_pipeline(
    pipeline_input: PipelineInput,
    pipeline_dao: PipelineDAO = Depends(),
) -> Pipeline:
    """
    Create a pipeline with the given input.

    :param id: create a pipeline with the given id.
    :return: dict[str, str].
    """
    id = await pipeline_dao.create_pipeline_model(
        input_schema_id=pipeline_input.input_schema_id,
        output_schema_id=pipeline_input.output_schema_id,
    )
    pipeline = await pipeline_dao.get_pipeline_model(str(id))

    if not pipeline or not pipeline.input_schema or not pipeline.output_schema:
        return {
            "error": f"Input or output schema not found for pipeline with id {id}.",
        }

    httpx.post(
        "https://automation.topo.io/webhook/11136b88-f235-4597-b9f6-48b3959c2388",
        data={
            "input_format": pipeline.input_schema.value,
            "output_format": pipeline.output_schema.value,
            "id": id,
        },
    )
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
