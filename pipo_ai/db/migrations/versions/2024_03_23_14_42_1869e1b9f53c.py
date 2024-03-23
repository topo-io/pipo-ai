"""empty message

Revision ID: 1869e1b9f53c
Revises: 819cbf6e030b
Create Date: 2024-03-23 14:42:38.830056

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1869e1b9f53c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pipeline",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("pipeline")
    # ### end Alembic commands ###
