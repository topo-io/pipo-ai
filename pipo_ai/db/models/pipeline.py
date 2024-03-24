from typing import TYPE_CHECKING

from sqlalchemy import ForeignKeyConstraint, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from pipo_ai.db.base import Base

if TYPE_CHECKING:
    from pipo_ai.db.models.json_schema import JSONSchema


class Pipeline(Base):
    __tablename__ = "pipeline"
    __table_args__ = (
        ForeignKeyConstraint(
            ["input_schema_id"],
            ["json_schema.id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["output_schema_id"],
            ["json_schema.id"],
            ondelete="CASCADE",
        ),
    )

    id: Mapped[Uuid] = mapped_column(
        Uuid, primary_key=True, default=func.uuid_generate_v4()
    )
    code: Mapped[Text] = mapped_column(Text, nullable=True)

    # Relationships
    input_schema_id: Mapped[Uuid] = mapped_column(Uuid)
    input_schema: Mapped["JSONSchema"] = relationship(
        "JSONSchema", foreign_keys=[input_schema_id]
    )

    output_schema_id: Mapped[Uuid] = mapped_column(Uuid)
    output_schema: Mapped["JSONSchema"] = relationship(
        "JSONSchema", foreign_keys=[output_schema_id]
    )
