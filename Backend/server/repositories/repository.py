from typing import Any
from sqlalchemy.orm import Session
from server.models.base import BaseModel
from server.models.users import Users


class Repository:
    """Store Access"""
    def __init__(self, db: Session, model: BaseModel):
        self.db = db
        self._Model = model

    async def add(self, entity: dict):
        """Creates a new entity and persists it in the database"""
        try:
            new_entity = self._Model(**entity)
            self.db.add(new_entity)
            self.db.commit()
            self.db.refresh(new_entity)
            return new_entity
        except Exception as e:
            self.db.rollback()
            raise e

    async def save(self, entity: BaseModel, data: dict):
        try:
            if data:
                for k, v in data.items():
                    setattr(entity, k, v)
            if not entity.id:
                self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_by_id(self, id: str):
        try:
            entity = self.db.query(self._Model).filter(self._Model == id)
            if entity:
                return entity.first()
            return None
        except Exception as e:
            raise e
        
    async def get_by_attr(self, attr: dict[str, str | Any]):
        try:
            entity = self.db.query(self._Model).filter_by(**attr)
            if entity:
                return entity.first()
            return None
        except Exception as e:
            raise e

    async def delete(self, entity: BaseModel) -> bool:
        try:
            self.db.delete(entity)
            self.db.commit()
        except Exception as e:
            raise e
        return True
    
    async def exists(self, filter: dict) -> bool:
        entity = self.db.query(self._Model).filter_by(**filter).first()
        return True if entity else False
