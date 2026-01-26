from logging.config import fileConfig

from sqlalchemy import engine_from_config, text
from sqlalchemy import pool

from alembic import context

from server.config import Base, app_configs

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline(database_url: str) -> None:
    """Run migrations in 'offline' mode for a specific database."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(database_url: str, schema: str) -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=database_url,
    )

    with connectable.connect() as connection:
        # 1. Create schema and set the search path so models find their home
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        connection.execute(text(f'SET search_path TO "{schema}"'))
        connection.commit()  # Ensure schema creation is committed before proceeding

        # 2. Define a filter to prevent Alembic from touching other schemas
        def include_object(object, name, type_, reflected, compare_to):
            if type_ == "table" and object.schema != schema:
                return False
            return True

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,  # Use the filter
            version_table_schema=schema,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            print("starting migrations...")
            context.run_migrations()


# def run_migrations() -> None:
#     """Run migrations for all configured databases."""
config.set_main_option("sqlalchemy.url", app_configs.DB.LIVE_DATABASE)
print(f"Running migrations for database: {config.get_main_option("sqlalchemy.url")}")

if context.is_offline_mode():
    run_migrations_offline(config.get_main_option("sqlalchemy.url"))
else:
    run_migrations_online(
        config.get_main_option("sqlalchemy.url"), app_configs.DB.SCHEMA
    )


# run_migrations()
