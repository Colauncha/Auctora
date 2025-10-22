from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "66a2f05c1d92"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    schema = "auctora_dev"
    table = "users"
    column = "role"

    # Check if column already exists
    columns = [col["name"] for col in inspector.get_columns(table, schema=schema)]
    if column not in columns:
        op.add_column(
            table,
            sa.Column(
                column,
                postgresql.ENUM("CLIENT", "ADMIN", name="userroles", schema=schema),
                nullable=False,
            ),
            schema=schema,
        )


def downgrade() -> None:
    schema = "auctora_dev"
    table = "users"
    column = "role"

    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    columns = [col["name"] for col in inspector.get_columns(table, schema=schema)]

    if column in columns:
        op.drop_column(table, column, schema=schema)

        # Optionally drop the enum type too
        op.execute(text(f"DROP TYPE IF EXISTS {schema}.userroles"))
