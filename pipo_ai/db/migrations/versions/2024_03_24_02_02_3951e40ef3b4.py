"""empty message

Revision ID: 3951e40ef3b4
Revises: 7e2eb314ce0b
Create Date: 2024-03-24 02:02:46.029130

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3951e40ef3b4"
down_revision = "7e2eb314ce0b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("TRUNCATE TABLE pipeline CASCADE")
    op.execute("TRUNCATE TABLE json_schema CASCADE")
    op.drop_constraint(
        "json_schema_pipeline_id_fkey", "json_schema", type_="foreignkey"
    )
    op.drop_column("json_schema", "pipeline_id")
    op.add_column(
        "pipeline", sa.Column("input_schema_id", sa.Uuid(), nullable=False)
    )
    op.add_column(
        "pipeline", sa.Column("output_schema_id", sa.Uuid(), nullable=False)
    )
    op.create_foreign_key(
        None,
        "pipeline",
        "json_schema",
        ["output_schema_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None,
        "pipeline",
        "json_schema",
        ["input_schema_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "pipeline", type_="foreignkey")
    op.drop_constraint(None, "pipeline", type_="foreignkey")
    op.drop_column("pipeline", "output_schema_id")
    op.drop_column("pipeline", "input_schema_id")
    op.add_column(
        "json_schema",
        sa.Column(
            "pipeline_id", sa.UUID(), autoincrement=False, nullable=True
        ),
    )
    op.create_foreign_key(
        "json_schema_pipeline_id_fkey",
        "json_schema",
        "pipeline",
        ["pipeline_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###