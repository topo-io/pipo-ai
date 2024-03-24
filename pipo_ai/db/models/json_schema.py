from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    Uuid,
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from pipo_ai.db.base import Base

if TYPE_CHECKING:
    pass


class JsonSchemaTypeEnum(str, Enum):
    input = "input"
    output = "output"


class JSONSchema(Base):
    __tablename__ = "json_schema"

    id: Mapped[Uuid] = mapped_column(
        Uuid, primary_key=True, default=func.uuid_generate_v4()
    )
    value: Mapped[JSON] = mapped_column(JSON, nullable=False)
    type: Mapped[JsonSchemaTypeEnum] = mapped_column(
        SQLAlchemyEnum(JsonSchemaTypeEnum), nullable=False
    )
