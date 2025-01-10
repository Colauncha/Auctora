"""Changed sellers_id to users_id

Revision ID: 305a49167ad5
Revises: 3d4a95246d2f
Create Date: 2025-01-10 19:20:36.541785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '305a49167ad5'
down_revision: Union[str, None] = '3d4a95246d2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('users_id', sa.UUID(), nullable=False), schema='auctora_dev')
    op.drop_constraint('items_sellers_id_fkey', 'items', schema='auctora_dev', type_='foreignkey')
    op.create_foreign_key(None, 'items', 'users', ['users_id'], ['id'], source_schema='auctora_dev', referent_schema='auctora_dev')
    op.drop_column('items', 'sellers_id', schema='auctora_dev')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('sellers_id', sa.UUID(), autoincrement=False, nullable=False), schema='auctora_dev')
    op.drop_constraint(None, 'items', schema='auctora_dev', type_='foreignkey')
    op.create_foreign_key('items_sellers_id_fkey', 'items', 'users', ['sellers_id'], ['id'], source_schema='auctora_dev', referent_schema='auctora_dev')
    op.drop_column('items', 'users_id', schema='auctora_dev')
    # ### end Alembic commands ###
