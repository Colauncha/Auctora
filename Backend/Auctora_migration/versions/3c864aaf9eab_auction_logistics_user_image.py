"""auction-logistics user-image

Revision ID: 3c864aaf9eab
Revises: eb313b2e9734
Create Date: 2025-05-07 22:15:32.381467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c864aaf9eab'
down_revision: Union[str, None] = 'eb313b2e9734'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auctions', sa.Column('pickup_address', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('auctions', sa.Column('pickup_latitude', sa.Float(), nullable=True), schema='auctora_dev')
    op.add_column('auctions', sa.Column('pickup_longitude', sa.Float(), nullable=True), schema='auctora_dev')
    op.add_column('auctions', sa.Column('logistic_type', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('auctions', sa.Column('logistic_fee', sa.Float(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('image_link', sa.JSON(), nullable=True), schema='auctora_dev')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'image_link', schema='auctora_dev')
    op.drop_column('auctions', 'logistic_fee', schema='auctora_dev')
    op.drop_column('auctions', 'logistic_type', schema='auctora_dev')
    op.drop_column('auctions', 'pickup_longitude', schema='auctora_dev')
    op.drop_column('auctions', 'pickup_latitude', schema='auctora_dev')
    op.drop_column('auctions', 'pickup_address', schema='auctora_dev')
    # ### end Alembic commands ###
