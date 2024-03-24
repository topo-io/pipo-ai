"""empty message

Revision ID: 34ba6a12a1b1
Revises: 4c30b526b026
Create Date: 2024-03-23 19:21:27.974014

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "34ba6a12a1b1"
down_revision = "4c30b526b026"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "json_schema",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("input", "output", name="jsonschematypeenum"),
            nullable=False,
        ),
        sa.Column("pipeline_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("jsonschema")


def downgrade() -> None:
    op.create_table(
        "jsonschema",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "value",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "type",
            postgresql.ENUM("input", "output", name="jsonschematypeenum"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "pipeline_id", sa.UUID(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="jsonschema_pkey"),
    )
    op.drop_table("json_schema")
