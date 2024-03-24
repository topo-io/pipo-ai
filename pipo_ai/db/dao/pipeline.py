from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from pipo_ai.db.dependencies import get_db_session
from pipo_ai.db.models.pipeline import Pipeline


class PipelineDAO:
    """Class for accessing pipeline table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_pipeline_model(self, id: str) -> None:
        """
        Add single pipeline to session.

        :param id: id of a pipeline.
        """
        pipeline = Pipeline(id=id)
        self.session.add(pipeline)

    async def upsert_pipeline_model(self, id: str, code: str) -> None:
        """
        Update or insert single pipeline to session.

        :param code: code of a pipeline.
        :param id: id of a pipeline.
        """
        query = select(Pipeline).where(Pipeline.id == id)
        row = await self.session.execute(query)
        pipeline = row.scalars().first()
        if pipeline:
            pipeline.code = code
        else:
            pipeline = Pipeline(id=id, code=code)
            self.session.add(pipeline)
        await self.session.commit()

    async def get_pipeline_model_with_schemas(
        self, id: str
    ) -> Pipeline | None:
        """
        Get specific pipeline model with schemas.

        :param id: id of pipeline instance.
        :return: pipeline model.
        """
        query = (
            select(Pipeline)
            .where(Pipeline.id == id)
            .options(joinedload(Pipeline.json_schemas))
        )
        row = await self.session.execute(query)
        return row.scalars().first()

    async def get_pipeline_model(self, id: str) -> Pipeline | None:
        """
        Get specific pipeline model.

        :param id: id of pipeline instance.
        :return: pipeline model.
        """
        query = select(Pipeline).where(Pipeline.id == id)
        row = await self.session.execute(query)
        return row.scalars().first()
