from fastapi import Depends
from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from pipo_ai.db.dependencies import get_db_session
from pipo_ai.db.models.json_schema import JSONSchema


class JSONSchemaDAO:
    """Class for accessing JSONSchema table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_json_schema_model(
        self,
        type: str,
        schema: dict,
    ) -> Uuid:
        """
        Add single JSONSchema to session.

        :param type: type of JSONSchema instance (input or output).
        :param schema: schema of a JSONSchema.
        :param pipeline_id: id of a Pipeline.
        """
        json_schema = JSONSchema(type=type, value=schema)
        self.session.add(json_schema)
        await self.session.commit()
        return json_schema.id  # type: ignore

    async def get_json_schema_model(
        self,
        type: str,
        id: str | None = None,
    ) -> JSONSchema | None:
        """
        Get specific JSONSchema model.

        :param type: type of JSONSchema instance.
        :param pipeline_id: id of a Pipeline.
        :return: JSONSchema model.
        """
        query = select(JSONSchema).where(
            JSONSchema.id == id and JSONSchema.type == type
        )
        row = await self.session.execute(query)
        return row.scalars().first()
