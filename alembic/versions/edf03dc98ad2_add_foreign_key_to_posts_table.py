"""add foreign-key to posts table

Revision ID: edf03dc98ad2
Revises: a36d52947bb7
Create Date: 2024-10-04 03:53:37.215955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edf03dc98ad2'
down_revision = 'a36d52947bb7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['ID'], ondelete="CASCADE")
    
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
