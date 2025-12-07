import math
from typing import Any, Union
from functools import wraps

from sqlalchemy.orm import Session

from server.config.app_configs import app_configs
from server.models.base import BaseModel
from server.models.users import Users
from server.schemas import (
    GetUserSchema, GetCategorySchema,
    GetSubCategorySchema, GetItemSchema,
    PagedResponse, GetAuctionSchema,
    GetBidSchema
)
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404, ExcRaiser500
)
from server.utils.helpers import paginator
from server.utils.ex_inspect import ExtInspect


T = Union[
    GetUserSchema, GetCategorySchema,
    GetItemSchema, GetSubCategorySchema,
    GetAuctionSchema, GetBidSchema, BaseModel

]


def no_db_error(func):
    """
    Decorator to raise error if DB is not attached\
    for the Repository class methods
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].db:
            raise ExcRaiser500(detail='DB not found or attached')
        return func(*args, **kwargs)
    return wrapper


class Repository:
    """Store Access"""
    db: Session = None
    def __init__(self, model: BaseModel):
        self._Model = model
        self._inspect = ExtInspect(self.__class__.__name__)
        self.configs = app_configs

    def attachDB(self, db: Session):
        """Attach database session to the repository"""
        if not db:
            raise ExcRaiser(message='DB not found or attached')
        self.db = db
        return self

    @no_db_error
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
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
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
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def get_by_id(self, id: str):
        try:
            entity = self.db.query(self._Model).filter(self._Model.id == id).order_by(self._Model.id)
            if entity:
                return entity.first()
            raise ExcRaiser404(message='Entity not found')
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def get_by_attr(self, attr: dict[str, str | Any], many: bool = False):
        try:
            entity = self.db.query(self._Model).filter_by(**attr)
            if entity and not many:
                return entity.first()
            elif entity and many:
                return entity.all()
            return None
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def update(
            self,
            entity: T,
            data: dict = None
        ) -> T:
        """Updates entity"""
        try:
            entity_to_update = self.db.query(self._Model).filter_by(id=entity.id or str(entity.id))
            if entity_to_update is None:
                raise ExcRaiser404(message='Entity not found')
            entity_to_update.update(data, synchronize_session="evaluate")
            self.db.commit()
            return entity_to_update.all()
        except Exception as e:
            self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def update_jsonb(
        self,
        id: str,
        data: dict = None,
        new_slot: bool = True,
        model: BaseModel = Users,
        attr = 'referred_users',
    ):
        try:
            if not data:
                raise ValueError("Data cannot be None or empty")
            entity = self.db.query(model).filter_by(id=id).first()
            if entity is None:
                raise ExcRaiser404(message='Entity not found')

            if hasattr(entity, attr):
                if attr == 'conversation':
                    convo = list(entity.conversation or [])
                    convo.append(data)
                    setattr(entity, attr, convo)
                elif attr == 'referred_users' and new_slot:
                    setattr(entity, attr, data)
                    entity.referral_slots_used += 1
            else:
                raise ExcRaiser404(message="Attribute doesn't exist")


            self.db.add(entity)
            self.db.commit()
            return entity
        except Exception as e:
            self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def delete(self, entity: BaseModel) -> bool:
        try:
            self.db.delete(entity)
            self.db.commit()
            return True
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def exists(self, filter: dict) -> bool:
        entity = self.db.query(self._Model).filter_by(**filter).first()
        return True if entity else False

    @no_db_error
    def all(self):
        try:
            return self.db.query(self._Model).order_by(self._Model.created_at).all()
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def get_all(
        self,
        filter: dict = None,
        relative: bool = False,
        sort: str = 'created_at',
    ) -> PagedResponse:
    
        page = filter.pop('page') if (filter and filter.get('page')) else 1
        per_page = filter.pop('per_page') if (filter and filter.get('per_page')) else 10
        order = filter.pop('order') if (filter and filter.get('order')) else 'asc'
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
            order_by_clause = getattr(QueryModel, sort)
            if order == "asc":
                order_by_clause = order_by_clause.asc()
            else:
                order_by_clause = order_by_clause.desc()
            query = query.order_by(order_by_clause)
            results = query.limit(limit).offset(offset).all()
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
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

    @no_db_error
    async def count(self, filter: dict = None) -> int:
        try:
            if filter:
                total = self.db.query(self._Model).filter_by(**filter).count()
            else:
                total = self.db.query(self._Model).count()
            return total
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e
