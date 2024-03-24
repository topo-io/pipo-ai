"""empty message

Revision ID: dfc2a414b9ce
Revises: 34ba6a12a1b1
Create Date: 2024-03-23 20:11:06.603456

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "dfc2a414b9ce"
down_revision = "34ba6a12a1b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        None,
        "json_schema",
        "pipeline",
        ["pipeline_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "json_schema", type_="foreignkey")
    # ### end Alembic commands ###