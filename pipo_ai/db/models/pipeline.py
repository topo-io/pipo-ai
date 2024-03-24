from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text, Uuid
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from pipo_ai.db.base import Base

if TYPE_CHECKING:
    from pipo_ai.db.models.json_schema import JSONSchema


class Pipeline(Base):
    __tablename__ = "pipeline"

    id = Column(Uuid, primary_key=True, default=func.uuid_generate_v4())
    slug = Column(String, nullable=False, unique=True)
    code = Column(Text, nullable=False)

    # Relationships
    jsonschemas: Mapped[list["JSONSchema"]] = relationship(
        "JSONSchema", back_populates="pipeline"
    )
