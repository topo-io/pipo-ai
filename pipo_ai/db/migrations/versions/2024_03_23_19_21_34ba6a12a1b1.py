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
    op.rename_table("jsonschema", "json_schema")


def downgrade() -> None:
    op.rename_table("json_schema", "jsonschema")
