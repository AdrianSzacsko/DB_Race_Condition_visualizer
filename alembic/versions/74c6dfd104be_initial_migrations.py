"""initial migrations

Revision ID: 74c6dfd104be
Revises: 
Create Date: 2023-10-31 12:16:07.490495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '74c6dfd104be'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('accounts',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('amount', sa.NUMERIC(precision=12, scale=2), server_default=sa.text('0'),
                              autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='accounts_pkey')
                    )
    logs = op.create_table('logs',
                           sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                           sa.Column('date', sa.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False,
                                     nullable=True),
                           sa.Column('account_from', sa.INTEGER(), autoincrement=False, nullable=True),
                           sa.Column('amount_before', sa.NUMERIC(precision=12, scale=2), autoincrement=False,
                                     nullable=True),
                           sa.Column('amount', sa.NUMERIC(precision=12, scale=2), autoincrement=False, nullable=True),
                           sa.PrimaryKeyConstraint('id', name='logs_pkey')
                           )
    op.create_table('logs2',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('date', sa.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False,
                              nullable=True),
                    sa.Column('message', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('account', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('amount', sa.NUMERIC(precision=12, scale=2), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='logs2_pkey')
                    )


def downgrade() -> None:
    op.drop_table('logs')
    op.drop_table('logs2')
    op.drop_table('accounts')
