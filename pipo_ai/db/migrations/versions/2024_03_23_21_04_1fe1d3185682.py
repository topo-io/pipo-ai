"""empty message

Revision ID: 1fe1d3185682
Revises: 130bb420540a
Create Date: 2024-03-23 21:04:32.295183

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1fe1d3185682"
down_revision = "130bb420540a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("pipeline", "code", existing_type=sa.TEXT(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "pipeline", "code", existing_type=sa.TEXT(), nullable=False
    )
    # ### end Alembic commands ###
