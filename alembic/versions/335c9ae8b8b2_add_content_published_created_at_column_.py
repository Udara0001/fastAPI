"""add content,published,created_at column to posts table

Revision ID: 335c9ae8b8b2
Revises: c212df65be10
Create Date: 2023-02-11 09:51:40.390062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '335c9ae8b8b2'
down_revision = 'c212df65be10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content",sa.String(),nullable=False))
    op.add_column("posts",
                  sa.Column("published", sa.Boolean(), nullable=False,server_default='TRUE'))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.text('now()')))

    pass


def downgrade() :
    op.drop_column("posts","content")
    op.drop_column("posts", "published")
    op.drop_column("posts","created_at" )
    pass
