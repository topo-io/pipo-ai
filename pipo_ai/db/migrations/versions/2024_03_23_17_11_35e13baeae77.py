"""empty message

Revision ID: 35e13baeae77
Revises: 1869e1b9f53c
Create Date: 2024-03-23 17:11:30.852528

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "35e13baeae77"
down_revision = "1869e1b9f53c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
