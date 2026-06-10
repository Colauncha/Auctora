"""unique wallet_transaction reference_id

Revision ID: 144a82eab817
Revises: 838b8a269c59
Create Date: 2026-06-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '144a82eab817'
down_revision: Union[str, None] = '838b8a269c59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('wallet_transactions', schema='auctora_dev') as batch_op:
        batch_op.create_unique_constraint(
            'uq_wallet_transactions_reference_id',
            ['reference_id']
        )


def downgrade() -> None:
    with op.batch_alter_table('wallet_transactions', schema='auctora_dev') as batch_op:
        batch_op.drop_constraint(
            'uq_wallet_transactions_reference_id',
            type_='unique'
        )
