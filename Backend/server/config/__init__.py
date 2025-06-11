import cloudinary
from server.config.app_configs import app_configs
from server.config.database import Base, engine, RedisStorage, get_db
from server.config.notification_messages import notification_messages


__all__ = [
    'app_configs',
    'Base',
    'init_db',
    'sync_redis',
    'redis_store',
    'cloudinary',
]


cloudinary_init = cloudinary.config(
    cloud_name=app_configs.cloudinary.CLOUD_NAME,
    api_key=app_configs.cloudinary.API_KEY,
    api_secret=app_configs.cloudinary.API_SECRET,
)


def init_db():
    """Initialize the database"""
    Base.metadata.create_all(engine)


redis_store = RedisStorage()
sync_redis = redis_store.redis