from sqlalchemy import Column, String, Text, Uuid
from sqlalchemy.sql import func

from pipo_ai.db.base import Base


class Pipeline(Base):
    __tablename__ = "pipeline"

    id = Column(Uuid, primary_key=True, default=func.uuid_generate_v4())
    slug = Column(String, nullable=False)
    code = Column(Text, nullable=False)
