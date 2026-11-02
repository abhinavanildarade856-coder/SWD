"""add nonnegative account balance constraint

Revision ID: bd29a384f3e9
Revises: 
Create Date: 2026-11-02 16:26:32.091327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd29a384f3e9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_account_balance_nonnegative",
        "accounts",
        "balance >= 0"
    )


def downgrade() -> None:
    op.drop_constraint(
        "check_account_balance_nonnegative",
        "accounts",
        type_="check"
    )