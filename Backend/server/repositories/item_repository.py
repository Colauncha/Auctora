from sqlalchemy import UUID
from server.repositories.repository import Repository
from server.models.items import Items, Categories, Subcategory
from server.schemas import (
    GetCategorySchema, GetSubCategorySchema,
    GetItemSchema, CreateCategorySchema,
    CreateItemSchema, CreateSubCategorySchema
)

class ItemRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Items)

    async def get_by_seller_id(
            self, id: str|UUID, schema_mode: bool = False
        ) -> GetItemSchema | Items:
        items = await self.get_by_attr({'seller_id': id}, many=True)
        if items and schema_mode:
            _items = [GetItemSchema.model_validate(item) for item in items]
            return _items
        elif items and not schema_mode:
            return items
        return None


class CategoryRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Categories)

    def get_last_id(self) -> str:
        last_cat = self.all()
        if last_cat:
            return last_cat[-1].id


class SubCategoryRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Subcategory)

    def get_last_id(self) -> str:
        last_sub_cat = self.all()
        if last_sub_cat:
            return last_sub_cat[-1].id