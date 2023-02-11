"""create a posts table 

Revision ID: c212df65be10
Revises: 
Create Date: 2023-02-11 09:41:39.308490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c212df65be10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() :
    op.create_table("posts",
                    sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
                    sa.Column("title",sa.String(),nullable=False))
    pass


def downgrade() :
    op.drop_table("posts")
    pass
