from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    Column,
    ForeignKeyConstraint,
    Uuid,
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from pipo_ai.db.base import Base

if TYPE_CHECKING:
    from pipo_ai.db.models.pipeline import Pipeline


class JsonSchemaTypeEnum(str, Enum):
    input = "input"
    output = "output"


class JSONSchema(Base):
    __tablename__ = "json_schema"
    __table_args__ = (
        ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.id"],
            ondelete="CASCADE",
        ),
    )

    id = Column(Uuid, primary_key=True, default=func.uuid_generate_v4())
    value = Column(JSON, nullable=False)
    type = Column(SQLAlchemyEnum(JsonSchemaTypeEnum), nullable=False)

    # Relationships
    pipeline_id: Mapped[Uuid | None] = mapped_column(Uuid)
    pipeline: Mapped["Pipeline"] = relationship(
        "Pipeline", back_populates="json_schemas"
    )

    def __getitem__(self, key):
        return self[key]
