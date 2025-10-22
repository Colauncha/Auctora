import uuid
from datetime import datetime
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
    created_at = Column(DateTime(timezone=True), default=datetime.now().astimezone())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now().astimezone())

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
