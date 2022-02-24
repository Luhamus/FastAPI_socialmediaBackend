"""add revision table

Revision ID: 7fb31859972f
Revises: f18f4db81d80
Create Date: 2022-02-24 02:14:33.592965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fb31859972f'
down_revision = 'f18f4db81d80'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("password", sa.String(), nullable=False),
            sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email")
            )
    pass


def downgrade():
    op.drop_table("users")
    pass
