from sqlalchemy import UUID, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from server.repositories.repository import Repository, no_db_error
from server.models.items import Items, Categories, Subcategory
from server.schemas import GetItemSchema
from server.middlewares.exception_handler import ExcRaiser404

class ItemRepository(Repository):
    def __init__(self, db: AsyncSession = None):
        super().__init__(Items)
        if db:
            super().attachDB(db)

    @no_db_error
    async def add(self, entity: dict):
        category_ids = entity.pop('category_ids', [])
        sub_category_ids = entity.pop('sub_category_ids', [])
        try:
            new_item = Items(**entity)
            self.db.add(new_item)
            await self.db.flush()

            if category_ids:
                new_item.categories = (await self.db.execute(
                    select(Categories).filter(Categories.id.in_(category_ids))
                )).scalars().all()
            if sub_category_ids:
                new_item.sub_categories = (await self.db.execute(
                    select(Subcategory).filter(Subcategory.id.in_(sub_category_ids))
                )).scalars().all()

            await self.db.commit()
            await self.db.refresh(new_item)
            return new_item
        except Exception as e:
            await self.db.rollback()
            raise e

    @no_db_error
    async def update(self, entity, data: dict = None):
        category_ids = data.pop('category_ids', None) if data else None
        sub_category_ids = data.pop('sub_category_ids', None) if data else None
        try:
            item = (await self.db.execute(
                select(Items).filter_by(id=entity.id or str(entity.id))
            )).scalars().first()
            if item is None:
                raise ExcRaiser404(message='Item not found')

            if data:
                for k, v in data.items():
                    if v is not None:
                        setattr(item, k, v)

            if category_ids is not None:
                item.categories = (await self.db.execute(
                    select(Categories).filter(Categories.id.in_(category_ids))
                )).scalars().all()
            if sub_category_ids is not None:
                item.sub_categories = (await self.db.execute(
                    select(Subcategory).filter(Subcategory.id.in_(sub_category_ids))
                )).scalars().all()

            await self.db.commit()
            await self.db.refresh(item)
            return [item]
        except Exception as e:
            await self.db.rollback()
            raise e

    @no_db_error
    async def get_by_seller_id(
            self, id: str|UUID, schema_mode: bool = False
        ) -> GetItemSchema | Items:
        items = await self.get_by_attr({'users_id': id}, many=True)
        if items and schema_mode:
            _items = [GetItemSchema.model_validate(item) for item in items]
            return _items
        elif items and not schema_mode:
            return items
        return None


class CategoryRepository(Repository):
    def __init__(self, db: AsyncSession = None):
        super().__init__(Categories)
        if db:
            super().attachDB(db)

    @no_db_error
    async def count(self) -> dict[str, int]:
        try:
            categories = (await self.db.execute(
                select(func.count()).select_from(Categories)
            )).scalar() or 0
            sub_category = (await self.db.execute(
                select(func.count()).select_from(Subcategory)
            )).scalar() or 0

            return {
                'categories': categories,
                'sub_category': sub_category,

            }
        except Exception as e:
            print(f"Error in count: {e}")
            raise e

    @no_db_error
    def get_last_id(self) -> str:
        # SYNC: invoked from the sync column-default path (helpers.py id
        # generators) with a sync Session — must not touch the async API.
        last_cat = (
            self.db.query(self._Model)
            .order_by(self._Model.created_at)
            .all()
        )
        if last_cat:
            return last_cat[-1].id


class SubCategoryRepository(Repository):
    def __init__(self, db: AsyncSession = None):
        super().__init__(Subcategory)
        if db:
            super().attachDB(db)

    @no_db_error
    def get_last_id(self) -> str:
        # SYNC: see CategoryRepository.get_last_id.
        last_sub_cat = (
            self.db.query(self._Model)
            .order_by(self._Model.created_at)
            .all()
        )
        if last_sub_cat:
            return last_sub_cat[-1].id
