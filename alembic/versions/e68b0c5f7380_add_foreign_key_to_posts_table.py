"""Add foreign-key to posts table

Revision ID: e68b0c5f7380
Revises: 7fb31859972f
Create Date: 2022-02-24 02:21:51.623836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e68b0c5f7380'
down_revision = '7fb31859972f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False) )
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
            local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
