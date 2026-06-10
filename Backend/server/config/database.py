"""
database.py
Central database configuration and initialization module.
Ensures schema creation before table creation, and safe Base import order.
"""

import os
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine, schema, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
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
# Database Engine (sync — kept for auction_status_updater and legacy repos)
# -----------------------------------------------------------------------------
engine = (
    create_engine(app_configs.DB.TEST_DATABASE)
    if environment == "test"
    else create_engine(
        app_configs.DB.DATABASE_URL,
        pool_size=10,
        max_overflow=6,
        pool_recycle=600,
        pool_timeout=5,
        pool_pre_ping=True,
        isolation_level="READ COMMITTED",
    )
)

# -----------------------------------------------------------------------------
# Async Engine (target for all FastAPI request handling)
# -----------------------------------------------------------------------------
def _async_url(url: str) -> str:
    return (
        url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
           .replace("postgresql://", "postgresql+asyncpg://")
    )

async_engine = (
    None  # aiosqlite not wired up for test env; use sync engine in tests
    if environment == "test"
    else create_async_engine(
        _async_url(app_configs.DB.DATABASE_URL),
        pool_size=10,
        max_overflow=6,
        pool_recycle=600,
        pool_timeout=5,
        pool_pre_ping=True,
    )
)

# -----------------------------------------------------------------------------
# Declarative Base
# -----------------------------------------------------------------------------
if environment == "test":
    default_schema = "public"
else:
    default_schema = app_configs.DB.SCHEMA

Base = declarative_base(metadata=schema.MetaData(schema=default_schema))

# -----------------------------------------------------------------------------
# Session factories
# -----------------------------------------------------------------------------
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# expire_on_commit=False keeps ORM objects usable after commit without
# re-querying — essential for async where implicit lazy IO is not allowed.
AsyncSessionLocal = (
    None
    if async_engine is None
    else async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
)

# -----------------------------------------------------------------------------
# Schema + Table Initialization
# -----------------------------------------------------------------------------
def import_all_models():
    """Dynamically imports all model modules under `server.models`."""
    import server.models

    package = server.models
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if not module_name.startswith("__") or module_name not in ("base",):
            import_module(f"{package.__name__}.{module_name}")


def init_db():
    """
    Initializes the database schema and creates all tables (sync).
    Used by the auction_status_updater process and test setup.
    """
    import_all_models()
    with engine.begin() as conn:
        print(f"🗄️  Initializing database schema '{default_schema}'...")
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {default_schema}"))
        Base.metadata.create_all(bind=conn)
    print("✅ Registered models:", list(Base.metadata.tables.keys()))


async def init_db_async():
    """
    Initializes the database schema and creates all tables (async).
    Called from the FastAPI lifespan on startup.
    """
    import_all_models()
    assert async_engine is not None, "async_engine is not configured (test env?)"
    async with async_engine.begin() as conn:
        print(f"🗄️  Initializing database schema '{default_schema}'...")
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {default_schema}"))
        await conn.run_sync(Base.metadata.create_all)
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


# -----------------------------------------------------------------------------
# FastAPI dependency — sync (legacy; migrate repos to get_async_db in Phase 3)
# -----------------------------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------------
# FastAPI dependency — async (target for all new and migrated repos)
# -----------------------------------------------------------------------------
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    assert AsyncSessionLocal is not None, "AsyncSessionLocal not configured"
    async with AsyncSessionLocal() as session:
        yield session


# -----------------------------------------------------------------------------
# Redis
# -----------------------------------------------------------------------------
class RedisStorage:
    REDIS_URL = app_configs.DB.REDIS_URL

    def __init__(self) -> None:
        self.redis = self.get_redis()
        self.async_redis = None

    def get_redis(self) -> SyncRedis:
        return SyncRedis.from_url(url=self.REDIS_URL, decode_responses=True)

    async def get_async_redis(self) -> AsyncRedis:
        if self.async_redis is None:
            self.async_redis = await AsyncRedis.from_url(
                url=self.REDIS_URL, decode_responses=True
            )
        return self.async_redis

    async def get_pubsub_redis(self) -> AsyncRedis:
        """Dedicated async connection for pubsub — must not share general-purpose connection."""
        return await AsyncRedis.from_url(url=self.REDIS_URL, decode_responses=True)
