import math
from typing import Any, Type, Union
from sqlalchemy.orm import Session
from server.models.base import BaseModel
from server.models.users import Users
from server.schemas import (
    GetUserSchema, GetCategorySchema,
    GetSubCategorySchema, GetItemSchema,
    PagedResponse
)
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404
)
from server.utils.helpers import paginator


T = Union[
    GetUserSchema, GetCategorySchema,
    GetItemSchema, GetSubCategorySchema,

]


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
            entity = self.db.query(self._Model).filter(self._Model.id == id).order_by(self._Model.id)
            if entity:
                return entity.first()
            return None
        except Exception as e:
            raise e
        
    async def get_by_attr(self, attr: dict[str, str | Any], many: bool = False):
        try:
            entity = self.db.query(self._Model).filter_by(**attr)
            if entity and not many:
                return entity.first()
            elif entity and many:
                return entity.all()
            return None
        except Exception as e:
            raise e
        
    async def update(
            self,
            entity: T,
            data: dict = None
        ) -> T:
        """Updates entity"""
        try:
            entity_to_update = self.db.query(self._Model).filter_by(id=entity.id)
            if entity_to_update is None:
                raise ExcRaiser404(message='Entity not found')
            entity_to_update.update(data, synchronize_session="evaluate")
            self.db.commit()
            return entity_to_update.all()
        except Exception as e:
            self.db.rollback()
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

    def all(self):
        try:
            return self.db.query(self._Model).order_by(self._Model.id).all()
        except Exception as e:
            raise e
        
    async def get_all(self, filter: dict = None) -> PagedResponse:
    
        page = filter.pop('page') if (filter and filter.get('page')) else 1
        per_page = filter.pop('per_page') if (filter and filter.get('per_page')) else 10
        limit = per_page
        offset = paginator(page, per_page)
        QueryModel = self._Model

        try:
            if filter:
                query = self.db.query(QueryModel).filter_by(**filter)
                total = query.count()
            else:
                query = self.db.query(QueryModel)
                total = query.count()
            results = query.limit(limit).offset(offset).all()
        except Exception as e:
            raise e
        count = len(results)
        pages = math.ceil(total / limit) or 1
        return PagedResponse(
            data=results,
            pages=pages,
            page_number=page,
            per_page=limit,
            count=count,
            total=total,
        )