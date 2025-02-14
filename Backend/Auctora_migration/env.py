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
    """Run migrations in 'online' mode for a specific database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=database_url
    )

    def include_name(name, type_, parent_names):
        if type_ == "schema":
            return name in [schema]
        else:
            return True

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_name=include_name,
            include_schemas=True,
            compare_type=True,
            version_table_schema=schema,
        )
        connection.execute(
            text(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations() -> None:
    """Run migrations for all configured databases."""
    for db_config in app_configs.DB.all():
        database_url = db_config
        schema = app_configs.DB.SCHEMA

        config.set_main_option('sqlalchemy.url', database_url)

        if context.is_offline_mode():
            run_migrations_offline(database_url)
        else:
            run_migrations_online(database_url, schema)


run_migrations()
