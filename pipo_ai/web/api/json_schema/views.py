from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.json_schema import JSONSchemaDAO
from pipo_ai.services.json_schema import infer_json_schema
from pipo_ai.web.api.json_schema.schema import JSONSchema, JSONSchemaDTO

router = APIRouter()


@router.post("/from_input", response_model=JSONSchema)
async def create_json_schema(
    input_dict: dict,
    json_schema_dao: JSONSchemaDAO = Depends(),
) -> JSONSchema:
    json_schema_validator = infer_json_schema(input_dict)
    id = await json_schema_dao.create_json_schema_model(
        type="input", schema=json_schema_validator
    )
    return JSONSchema(id=str(id))


@router.post("/")
async def upsert_json_schema(
    input: JSONSchemaDTO,
    json_schema_dao: JSONSchemaDAO = Depends(),
) -> JSONSchema:
    """
    Create a JSON schema.

    :return: updated JSON schema.
    """

    id = await json_schema_dao.create_json_schema_model(
        schema=input.json_schema,
        type=input.type,
    )
    return JSONSchema(id=str(id))
