"""empty message

Revision ID: e9d5a4cf60c4
Revises: 35e13baeae77
Create Date: 2024-03-23 17:13:05.833003

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e9d5a4cf60c4"
down_revision = "35e13baeae77"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "pipeline", "id", server_default=sa.text("uuid_generate_v4()")
    )


def downgrade() -> None:
    op.alter_column("pipeline", "id", server_default=None)
