from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pipo_ai.db.dependencies import get_db_session
from pipo_ai.db.models.json_schema import JSONSchema


class JSONSchemaDAO:
    """Class for accessing JSONSchema table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_json_schema_model(
        self,
        pipeline_id: str,
        type: str,
        schema: dict,
    ) -> None:
        """
        Add single JSONSchema to session.

        :param schema: schema of a JSONSchema.
        :param slug: slug of a JSONSchema.
        """
        json_schema = JSONSchema(
            pipeline_id=pipeline_id, type=type, value=schema
        )
        self.session.add(json_schema)

    async def upsert_json_schema_model(
        self,
        pipeline_id: str,
        type: str,
        schema: dict,
    ) -> None:
        """
        Update or insert single JSONSchema to session.

        :param schema: schema of a JSONSchema.
        :param slug: slug of a JSONSchema.
        """
        query = select(JSONSchema).where(
            JSONSchema.pipeline_id == pipeline_id and JSONSchema.type == type
        )
        row = await self.session.execute(query)
        json_schema = row.scalars().first()
        if json_schema:
            json_schema.schema = schema
        else:
            json_schema = JSONSchema(
                pipeline_id=pipeline_id, type=type, value=schema
            )
            self.session.add(json_schema)

    async def get_json_schema_model(
        self, pipeline_id: str, type: str
    ) -> JSONSchema | None:
        """
        Get specific JSONSchema model.

        :param slug: slug of JSONSchema instance.
        :return: JSONSchema model.
        """
        query = select(JSONSchema).where(
            JSONSchema.pipeline_id == pipeline_id and JSONSchema.type == type
        )
        row = await self.session.execute(query)
        return row.scalars().first()
