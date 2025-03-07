"""updated user and auction models

Revision ID: ba8b3227ccde
Revises: e71a2bf71f95
Create Date: 2025-03-04 13:05:59.670412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba8b3227ccde'
down_revision: Union[str, None] = 'e71a2bf71f95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auctions', sa.Column('watchers', sa.Integer(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('acct_no', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('acct_name', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('bank_code', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('recipient_code', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('address', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('city', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('state', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('country', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('kyc_id_type', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('kyc_id_number', sa.String(), nullable=True), schema='auctora_dev')
    op.add_column('users', sa.Column('rating', sa.Float(), nullable=True), schema='auctora_dev')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'rating', schema='auctora_dev')
    op.drop_column('users', 'kyc_id_number', schema='auctora_dev')
    op.drop_column('users', 'kyc_id_type', schema='auctora_dev')
    op.drop_column('users', 'country', schema='auctora_dev')
    op.drop_column('users', 'state', schema='auctora_dev')
    op.drop_column('users', 'city', schema='auctora_dev')
    op.drop_column('users', 'address', schema='auctora_dev')
    op.drop_column('users', 'recipient_code', schema='auctora_dev')
    op.drop_column('users', 'bank_code', schema='auctora_dev')
    op.drop_column('users', 'acct_name', schema='auctora_dev')
    op.drop_column('users', 'acct_no', schema='auctora_dev')
    op.drop_column('auctions', 'watchers', schema='auctora_dev')
    # ### end Alembic commands ###
