import math
from typing import Any, Union
from functools import wraps

from sqlalchemy import select, update as sa_update, func
from sqlalchemy.ext.asyncio import AsyncSession

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
    """Store Access (async)"""
    db: AsyncSession = None
    def __init__(self, model: BaseModel):
        self._Model = model
        self._inspect = ExtInspect(self.__class__.__name__)
        self.configs = app_configs

    def attachDB(self, db: AsyncSession):
        """Attach database session to the repository"""
        self.db = db
        return self

    @no_db_error
    async def add(self, entity: dict, commit: bool = True):
        """Creates a new entity and persists it in the database.

        `commit=False` flushes the insert without ending the transaction,
        so callers can keep a `for_update` lock held across several writes
        and commit them all atomically.
        """
        try:
            new_entity = self._Model(**entity)

            self.db.add(new_entity)
            if commit:
                await self.db.commit()
                await self.db.refresh(new_entity)
            else:
                await self.db.flush()
            return new_entity
        except Exception as e:
            await self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                print(e)
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
            await self.db.commit()
            await self.db.refresh(entity)
            return entity
        except Exception as e:
            await self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def get_by_id(self, id: str, for_update: bool = False):
        """
        `for_update=True` issues `SELECT ... FOR UPDATE`, taking a row lock
        that is held until the current transaction commits or rolls back.
        Use it to serialize concurrent read-check-write sequences (e.g. bid
        placement) against the same row.
        """
        try:
            stmt = (
                select(self._Model)
                .filter(self._Model.id == id)
                .order_by(self._Model.id)
            )
            if for_update:
                stmt = stmt.with_for_update()
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def get_by_attr(self, attr: dict[str, str | Any], many: bool = False):
        try:
            result = await self.db.execute(
                select(self._Model).filter_by(**attr)
            )
            if many:
                return result.scalars().all()
            return result.scalars().first()
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def update(
            self,
            entity: T,
            data: dict = None,
            commit: bool = True,
        ) -> T:
        """Updates entity.

        `commit=False` flushes the update without ending the transaction,
        letting callers batch several writes under one lock and commit
        them together.
        """
        try:
            _id = entity.id or str(entity.id)
            exists = (await self.db.execute(
                select(self._Model).filter_by(id=_id)
            )).scalars().first()
            if exists is None:
                raise ExcRaiser404(message='Entity not found')
            await self.db.execute(
                sa_update(self._Model)
                .where(self._Model.id == _id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            if commit:
                await self.db.commit()
            else:
                await self.db.flush()
            refreshed = await self.db.execute(
                select(self._Model).filter_by(id=_id)
            )
            return refreshed.scalars().all()
        except Exception as e:
            await self.db.rollback()
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
            entity = (await self.db.execute(
                select(model).filter_by(id=id)
            )).scalars().first()
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
            await self.db.commit()
            return entity
        except Exception as e:
            await self.db.rollback()
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def delete(self, entity: BaseModel) -> bool:
        try:
            await self.db.delete(entity)
            await self.db.commit()
            return True
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e

    @no_db_error
    async def exists(self, filter: dict) -> bool:
        result = await self.db.execute(
            select(self._Model).filter_by(**filter)
        )
        return result.scalars().first() is not None

    @no_db_error
    async def all(self):
        try:
            result = await self.db.execute(
                select(self._Model).order_by(self._Model.created_at)
            )
            return result.scalars().all()
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
            stmt = select(QueryModel)
            if filter:
                stmt = stmt.filter_by(**filter)
            total = (await self.db.execute(
                select(func.count()).select_from(stmt.subquery())
            )).scalar() or 0

            order_by_clause = getattr(QueryModel, sort)
            order_by_clause = (
                order_by_clause.asc() if order == "asc"
                else order_by_clause.desc()
            )
            stmt = stmt.order_by(order_by_clause).limit(limit).offset(offset)
            results = (await self.db.execute(stmt)).scalars().all()
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
            stmt = select(func.count()).select_from(self._Model)
            if filter:
                stmt = select(func.count()).select_from(
                    select(self._Model).filter_by(**filter).subquery()
                )
            total = (await self.db.execute(stmt)).scalar() or 0
            return total
        except Exception as e:
            if self.configs.DEBUG:
                self._inspect.info()
                raise e
            raise e
