"""empty message

Revision ID: 4babe970374b
Revises: 31955a9b7348
Create Date: 2023-10-19 17:46:35.219408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4babe970374b"
down_revision = "31955a9b7348"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("registration", sa.Column("language_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "registration", "language", ["language_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "registration", type_="foreignkey")
    op.drop_column("registration", "language_id")
    # ### end Alembic commands ###
