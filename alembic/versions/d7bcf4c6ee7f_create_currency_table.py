"""create currency  table

Revision ID: d7bcf4c6ee7f
Revises: 
Create Date: 2023-05-04 19:06:58.185315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7bcf4c6ee7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'currency',
        sa.Column('code', sa.String, primary_key=True, index=True),
        sa.Column('title', sa.String),
    )


def downgrade() -> None:
    op.drop_table('currency')
