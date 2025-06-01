import uuid
from datetime import datetime
from server.config import Base
from sqlalchemy import Column, DateTime, UUID 


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.now().astimezone())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now().astimezone())

    def to_dict(self):
        dict = {}
        for attr, vals in self.__dict__.items():
            if attr.startswith('_') or attr == 'hash_password':
                pass
            else:
                dict[attr] = vals
        return dict
