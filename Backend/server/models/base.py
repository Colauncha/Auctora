import uuid
from datetime import datetime, timezone
from server.config.app_configs import app_configs
from server.config import Base
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.orm import declared_attr


class BaseModel(Base):
    __abstract__ = True
    @declared_attr
    def __table_args__(cls):
        from server.config import app_configs
        return {"schema": app_configs.DB.SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self, exclude: list = None) -> dict:
        dict = {}
        for attr, vals in self.__dict__.items():
            if attr.startswith('_') or attr == 'hash_password':
                continue
            elif exclude and attr in exclude:
                continue
            else:
                dict[attr] = vals
        return dict
