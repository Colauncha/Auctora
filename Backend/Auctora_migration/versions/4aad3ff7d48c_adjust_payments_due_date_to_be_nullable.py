"""adjust payments.due_date to be nullable

Revision ID: 4aad3ff7d48c
Revises: aa4d4a55edbb
Create Date: 2025-05-13 16:03:00.632690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aad3ff7d48c'
down_revision: Union[str, None] = 'aa4d4a55edbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
