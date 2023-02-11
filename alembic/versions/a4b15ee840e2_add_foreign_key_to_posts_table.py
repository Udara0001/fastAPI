"""add foreign key to posts table

Revision ID: a4b15ee840e2
Revises: cd8606754c6b
Create Date: 2023-02-11 10:56:26.519511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4b15ee840e2'
down_revision = 'cd8606754c6b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users-fk',source_table='posts', referent_table='users',local_cols= ['owner_id'],remote_cols= ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users-fk',table_name='posts')
    op.drop_column("posts","owner_id")

    pass
