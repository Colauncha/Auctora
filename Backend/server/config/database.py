"""
database.py
Central database configuration and initialization module.
Ensures schema creation before table creation, and safe Base import order.
"""

import os
from contextlib import contextmanager
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine, schema, text, event
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    scoped_session,
    Session,
)
from redis import StrictRedis as SyncRedis
from redis.asyncio import StrictRedis as AsyncRedis
from dotenv import load_dotenv
from importlib import import_module
import pkgutil

from server.config.app_configs import app_configs

# -----------------------------------------------------------------------------
# Load environment
# -----------------------------------------------------------------------------
load_dotenv()
environment = os.getenv("ENV", "test")
print(f"🔧 Environment: {environment}")

# -----------------------------------------------------------------------------
# Database Engine
# -----------------------------------------------------------------------------
if environment == "test":
    DATABASE_URL = app_configs.DB.TEST_DATABASE
    print("🧪 Using TEST database")
else:
    DATABASE_URL = app_configs.DB.DATABASE_URL
    print(f"🏗️ Using DATABASE: {DATABASE_URL}")

# engine = create_engine(
#     DATABASE_URL,
#     pool_size=10 if environment != "test" else None,
#     max_overflow=5 if environment != "test" else None,
#     pool_recycle=3600 if environment != "test" else None,
#     isolation_level="READ COMMITTED",
# )

engine = (
    create_engine(app_configs.DB.TEST_DATABASE)
    if environment == "test"
    else create_engine(
        app_configs.DB.DATABASE_URL,
        pool_size=10,
        max_overflow=6,
        pool_recycle=600,
        pool_pre_ping=True,
        isolation_level="READ COMMITTED",
    )
)


# @event.listens_for(engine, "checkout")
# def receive_checkout(dbapi_connection, connection_record, connection_proxy):
#     print(f"Connection checked out! Current status: {engine.pool.status()}")


# @event.listens_for(engine, "checkin")
# def receive_checkin(dbapi_connection, connection_record):
#     print(f"Connection returned! Current status: {engine.pool.status()}")


# -----------------------------------------------------------------------------
# Declarative Base
# -----------------------------------------------------------------------------
if environment == "test":
    default_schema = "public"
else:
    default_schema = app_configs.DB.SCHEMA

Base = declarative_base(metadata=schema.MetaData(schema=default_schema))

# -----------------------------------------------------------------------------
# Session
# -----------------------------------------------------------------------------
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.query = scoped_session(SessionLocal).query_property()

# -----------------------------------------------------------------------------
# Schema + Table Initialization
# -----------------------------------------------------------------------------
def import_all_models():
    """Dynamically imports all model modules under `server.models`."""
    import server.models  # ensure models package is imported

    package = server.models
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if not module_name.startswith("__") or module_name not in ("base",):
            import_module(f"{package.__name__}.{module_name}")


def init_db():
    """
    Initializes the database schema and creates all tables.
    Ensures:
    1. Schema exists
    2. All models are imported and registered
    3. Tables and ENUMs are created in the correct schema, in the same transaction
    """
    # Import models AFTER Base is defined, BEFORE schema creation
    import_all_models()

    with engine.begin() as conn:
        print(f"🗄️  Initializing database schema '{default_schema}'...")
        # 1️⃣ Create schema (inside same transaction)
        res = conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {default_schema}"))
        print(f"✅ Ensured schema '{res}' exists.")

        # 2️⃣ Bind Base to this same connection so ENUMs are created correctly
        Base.metadata.create_all(bind=conn)

    print("✅ Registered models:", list(Base.metadata.tables.keys()))


def recreate_db():
    """Drops and recreates the entire database schema. Use with caution."""
    if environment != "production":
        with engine.begin() as conn:
            print(f"⚠️  Dropping database schema '{default_schema}'...")
            Base.metadata.drop_all(bind=conn)
            print(f"✅ Creating database schema '{default_schema}'...")
            Base.metadata.create_all(bind=conn)
    else:
        print("⛔ Cannot recreate database in production environment!")


# Dependency for FastAPI
# -----------------------------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    """Yields a database session for dependency injection."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.expire_on_commit
        db.close()


# def get_db() -> Iterator[Session]:
#     try:
#         db: Session = SessionLocal()
#         yield db
#     except Exception as e:
#         raise e
#     finally:
#         db.expire_on_commit
#         db.close()


class RedisStorage:
    REDIS_URL = app_configs.DB.REDIS_URL
    def __init__(self) -> None:
        self.redis = self.get_redis()
        self.async_redis = None

    def get_redis(self) -> SyncRedis:
        """Get a synchronous Redis connection."""
        redis = SyncRedis.from_url(
            url=self.REDIS_URL, decode_responses=True
        )
        return redis

    async def get_async_redis(self) -> AsyncRedis:
        """Get an asynchronous Redis connection."""
        if self.async_redis is None:
            self.async_redis = await AsyncRedis.from_url(
                url=self.REDIS_URL, decode_responses=True
            )
        return self.async_redis

    async def get_pubsub_redis(self) -> AsyncRedis:
        """Get a dedicated async Redis connection for pubsub use.
        Pubsub changes the connection state, so it must not share the
        general-purpose async connection."""
        return await AsyncRedis.from_url(url=self.REDIS_URL, decode_responses=True)
