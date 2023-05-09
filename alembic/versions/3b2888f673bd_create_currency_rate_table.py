"""create currency_rate  table

Revision ID: 3b2888f673bd
Revises: d7bcf4c6ee7f
Create Date: 2023-05-04 19:08:09.853378

"""
from datetime import datetime as dt

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '3b2888f673bd'
down_revision = 'd7bcf4c6ee7f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'currency_rate',
        sa.Column('currency_left', sa.String, sa.ForeignKey('currency.code')),
        sa.Column('currency_right', sa.String, sa.ForeignKey('currency.code')),
        sa.Column('rate', sa.Float),
        sa.Column('updated_at', sa.DateTime, default=dt.now()),
        sa.PrimaryKeyConstraint('currency_left', 'currency_right'),
    )


def downgrade() -> None:
    op.drop_table('currency_rate')
