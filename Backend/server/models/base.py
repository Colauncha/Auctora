import enum
import logging
import uuid
from datetime import datetime, timezone
from server.config.app_configs import app_configs
from server.config import Base
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.orm import declared_attr
from typing import List

logger = logging.getLogger(__name__)

class BaseModel(Base):
    __abstract__ = True
    @declared_attr
    def __table_args__(cls):
        from server.config import app_configs
        return {"schema": app_configs.DB.SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

    def _to_dict_value(self, vals, _seen: set, for_update: bool = False):
        if isinstance(vals, BaseModel):
            key = (type(vals), vals.id)
            if key in _seen:
                return {"id": vals.id}
            return vals.to_dict(_seen=_seen, for_update=for_update)
        elif isinstance(vals, list):
            return [
                self._to_dict_value(item, _seen, for_update=for_update) for item in vals
            ]
        elif isinstance(vals, enum.Enum):
            if for_update:
                return vals
            return vals.value
        elif isinstance(vals, uuid.UUID):
            if for_update:
                return vals
            return str(vals)
        elif isinstance(vals, datetime):
            if for_update:
                return vals
            return str(vals)
        else:
            return vals

    def to_dict(
        self, exclude: list = None, _seen: set = None, for_update: bool = False
    ) -> dict:
        try:
            _seen = _seen if _seen is not None else set()
            key = (type(self), self.id)
            _seen.add(key)
            result = {}
            for attr, vals in self.__dict__.items():
                if attr.startswith("_") or attr == "hash_password":
                    continue
                elif exclude and attr in exclude:
                    continue
                else:
                    result[attr] = self._to_dict_value(
                        vals, _seen, for_update=for_update
                    )
            _seen.discard(key)
            return result
        except Exception as e:
            logger.error(f"Error serializing {type(self).__name__}: {e}")
            raise e
