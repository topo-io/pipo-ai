from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pipo_ai.db.dependencies import get_db_session
from pipo_ai.db.models.json_schema import JSONSchema


class JSONSchemaDAO:
    """Class for accessing JSONSchema table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_json_schema_model(self, schema: dict, slug: str) -> None:
        """
        Add single JSONSchema to session.

        :param schema: schema of a JSONSchema.
        :param slug: slug of a JSONSchema.
        """
        json_schema = JSONSchema(schema=schema, slug=slug)
        self.session.add(json_schema)

    async def upsert_json_schema_model(self, schema: dict, slug: str) -> None:
        """
        Update or insert single JSONSchema to session.

        :param schema: schema of a JSONSchema.
        :param slug: slug of a JSONSchema.
        """
        query = select(JSONSchema).where(JSONSchema.slug == slug)
        row = await self.session.execute(query)
        json_schema = row.scalars().first()
        if json_schema:
            json_schema.schema = schema
        else:
            json_schema = JSONSchema(schema=schema, slug=slug)
            self.session.add(json_schema)

    async def get_json_schema_model(self, slug: str) -> JSONSchema | None:
        """
        Get specific JSONSchema model.

        :param slug: slug of JSONSchema instance.
        :return: JSONSchema model.
        """
        query = select(JSONSchema).where(JSONSchema.slug == slug)
        row = await self.session.execute(query)
        return row.scalars().first()

    async def filter(
        self,
        slug: str | None = None,
    ) -> list:
        """
        Get specific JSONSchema models.

        :param slug: slug of JSONSchema instance.
        :return: JSONSchema models.
        """
        query = select(JSONSchema)
        if slug:
            query = query.where(JSONSchema.slug == slug)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
