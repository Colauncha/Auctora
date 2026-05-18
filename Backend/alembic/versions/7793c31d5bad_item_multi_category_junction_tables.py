"""item multi-category junction tables

Revision ID: 7793c31d5bad
Revises: 838b8a269c59
Create Date: 2026-05-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '7793c31d5bad'
down_revision: Union[str, None] = '838b8a269c59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = 'auctora_dev'


def upgrade() -> None:
    # 1. Create junction tables
    op.create_table(
        'item_categories',
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], [f'{SCHEMA}.items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], [f'{SCHEMA}.categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('item_id', 'category_id'),
        schema=SCHEMA,
    )
    op.create_table(
        'item_subcategories',
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sub_category_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], [f'{SCHEMA}.items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sub_category_id'], [f'{SCHEMA}.subcategories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('item_id', 'sub_category_id'),
        schema=SCHEMA,
    )

    # 2. Migrate existing single-category data into the junction tables
    op.execute(f"""
        INSERT INTO {SCHEMA}.item_categories (item_id, category_id)
        SELECT id, category_id
        FROM {SCHEMA}.items
        WHERE category_id IS NOT NULL
    """)
    op.execute(f"""
        INSERT INTO {SCHEMA}.item_subcategories (item_id, sub_category_id)
        SELECT id, sub_category_id
        FROM {SCHEMA}.items
        WHERE sub_category_id IS NOT NULL
    """)

    # 3. Drop the old FK columns from items
    with op.batch_alter_table('items', schema=SCHEMA) as batch_op:
        batch_op.drop_constraint('items_category_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('items_sub_category_id_fkey', type_='foreignkey')
        batch_op.drop_column('category_id')
        batch_op.drop_column('sub_category_id')


def downgrade() -> None:
    # 1. Re-add the old FK columns (nullable during migration)
    with op.batch_alter_table('items', schema=SCHEMA) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sub_category_id', sa.String(), nullable=True))
        batch_op.create_foreign_key(
            'items_category_id_fkey', 'categories', ['category_id'], ['id'],
            referent_schema=SCHEMA,
        )
        batch_op.create_foreign_key(
            'items_sub_category_id_fkey', 'subcategories', ['sub_category_id'], ['id'],
            referent_schema=SCHEMA,
        )

    # 2. Restore one category/subcategory per item from the junction tables
    op.execute(f"""
        UPDATE {SCHEMA}.items i
        SET category_id = (
            SELECT ic.category_id
            FROM {SCHEMA}.item_categories ic
            WHERE ic.item_id = i.id
            LIMIT 1
        )
    """)
    op.execute(f"""
        UPDATE {SCHEMA}.items i
        SET sub_category_id = (
            SELECT isc.sub_category_id
            FROM {SCHEMA}.item_subcategories isc
            WHERE isc.item_id = i.id
            LIMIT 1
        )
    """)

    # 3. Drop junction tables
    op.drop_table('item_subcategories', schema=SCHEMA)
    op.drop_table('item_categories', schema=SCHEMA)
