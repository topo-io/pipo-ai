from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pipo_ai.db.dependencies import get_db_session
from pipo_ai.db.models.pipeline import Pipeline


class PipelineDAO:
    """Class for accessing pipeline table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_pipeline_model(self, code: str, slug: str) -> None:
        """
        Add single pipeline to session.

        :param code: code of a pipeline.
        :param slug: slug of a pipeline.
        """
        self.session.add(Pipeline(code=code, slug=slug))

    async def filter(
        self,
        slug: str | None = None,
    ) -> list:
        """
        Get specific pipeline model.

        :param slug: slug of pipeline instance.
        :return: pipeline models.
        """
        query = select(Pipeline)
        if slug:
            query = query.where(Pipeline.slug == slug)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
