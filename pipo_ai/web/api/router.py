from fastapi.routing import APIRouter

from pipo_ai.web.api import docs, echo, monitoring, pipeline, json_schema

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(
    pipeline.router, prefix="/pipeline", tags=["pipeline"]
)
api_router.include_router(
    json_schema.router, prefix="/json_schema", tags=["json_schema"]
)
