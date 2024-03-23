from sqlalchemy import Column, String, Text, Uuid

from pipo_ai.db.base import Base


class Pipeline(Base):
    __tablename__ = "pipeline"

    id = Column(Uuid, primary_key=True)
    slug = Column(String, nullable=False)
    code = Column(Text, nullable=False)
