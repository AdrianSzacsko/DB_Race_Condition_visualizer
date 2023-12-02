"""add users

Revision ID: 54b489d7aa88
Revises: 74c6dfd104be
Create Date: 2023-10-31 12:20:43.512730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '54b489d7aa88'
down_revision: Union[str, None] = '74c6dfd104be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table('users',
                            sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                            sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                            sa.Column('amount', sa.NUMERIC(precision=12, scale=2), server_default=sa.text('0'),
                                      autoincrement=False, nullable=True),
                            sa.PrimaryKeyConstraint('id', name='users_pkey')
                            )
    op.bulk_insert(table, [
        {
            'username': 'Adam',
            'amount': 750
        },
        {
            'username': 'Oliver',
            'amount': 750
        },
    ])


def downgrade() -> None:
    op.drop_table('users')
