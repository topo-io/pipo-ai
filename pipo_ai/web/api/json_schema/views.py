from fastapi import APIRouter
from fastapi.param_functions import Depends

from pipo_ai.db.dao.json_schema import JSONSchemaDAO
from pipo_ai.services.json_schema import infer_json_schema
from pipo_ai.web.api.json_schema.schema import JSONSchemaSlug

router = APIRouter()


@router.post("/{slug}/from_input", response_model=JSONSchemaSlug)
async def create_json_schema(
    slug: str,
    input_dict: dict,
    json_schema_dao: JSONSchemaDAO = Depends(),
) -> JSONSchemaSlug:
    json_schema_validator = infer_json_schema(input_dict)
    print(json_schema_validator)
    json_schema_dao.create_json_schema_model(
        pipeline_id=slug, type="input", schema={}
    )
    return JSONSchemaSlug(slug=slug)
