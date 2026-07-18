"""merge heads

Revision ID: f38995b1d8c5
Revises: 144a82eab817, 7793c31d5bad
Create Date: 2026-07-18 23:01:36.272790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f38995b1d8c5'
down_revision: Union[str, None] = ('144a82eab817', '7793c31d5bad')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
