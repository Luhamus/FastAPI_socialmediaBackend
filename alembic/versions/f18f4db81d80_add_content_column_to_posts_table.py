"""add content column to posts table

Revision ID: f18f4db81d80
Revises: 19d57d527c14
Create Date: 2022-02-24 02:03:54.409749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f18f4db81d80'
down_revision = '19d57d527c14'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False) )
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
