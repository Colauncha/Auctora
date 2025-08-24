from sqlalchemy import UUID
from server.repositories.repository import Repository, no_db_error
from server.models.items import Items, Categories, Subcategory
from server.schemas import GetItemSchema

class ItemRepository(Repository):
    def __init__(self):
        super().__init__(Items)

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
    def __init__(self):
        super().__init__(Categories)

    @no_db_error
    async def count(self) -> dict[str, int]:
        try:
            categories = self.db.query(Categories).count()
            sub_category = self.db.query(Subcategory).count()

            return {
                'categories': categories,
                'sub_category': sub_category,

            }
        except Exception as e:
            print(f"Error in count: {e}")
            raise e

    def get_last_id(self) -> str:
        last_cat = self.all()
        if last_cat:
            return last_cat[-1].id


class SubCategoryRepository(Repository):
    def __init__(self):
        super().__init__(Subcategory)

    def get_last_id(self) -> str:
        last_sub_cat = self.all()
        if last_sub_cat:
            return last_sub_cat[-1].id