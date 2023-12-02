"""add triggers

Revision ID: f71fda7b7498
Revises: 54b489d7aa88
Create Date: 2023-10-31 14:08:06.996348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f71fda7b7498'
down_revision: Union[str, None] = '54b489d7aa88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


create_trigger = """
CREATE OR REPLACE FUNCTION user_update_trigger()
RETURNS TRIGGER AS $$
BEGIN
  -- Insert a new row into the logs table on each update of the users table
  INSERT INTO logs (date, account_from, amount_before, amount)
  VALUES (NOW(), OLD.id, OLD.amount, NEW.amount - OLD.amount);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_update
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION user_update_trigger();
"""

drop_trigger = """
drop trigger user_update on users;
"""


def upgrade() -> None:
    op.execute(create_trigger)
    pass


def downgrade() -> None:
    op.execute(drop_trigger)
    pass
