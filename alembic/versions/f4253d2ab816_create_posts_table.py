"""Create posts table

Revision ID: f4253d2ab816
Revises: 
Create Date: 2024-10-03 04:02:10.062570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4253d2ab816'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
