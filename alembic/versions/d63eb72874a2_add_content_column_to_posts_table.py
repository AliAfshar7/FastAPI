"""add content column to posts table

Revision ID: d63eb72874a2
Revises: f4253d2ab816
Create Date: 2024-10-03 06:02:50.550363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd63eb72874a2'
down_revision = 'f4253d2ab816'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
