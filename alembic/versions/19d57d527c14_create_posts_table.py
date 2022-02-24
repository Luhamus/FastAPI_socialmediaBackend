"""create posts table

Revision ID: 19d57d527c14
Revises: 
Create Date: 2022-02-24 01:18:04.684095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19d57d527c14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True ),
            sa.Column("title", sa.String(), nullable=False) )
    pass


def downgrade():
    op.drop_table('posts')
    pass
