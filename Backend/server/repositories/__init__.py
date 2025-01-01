from server.repositories.repository import Repository
from server.repositories.user_repository import UserRepository
from server.repositories.item_repository import (
    ItemRepository, CategoryRepository,
    SubCategoryRepository
)
from sqlalchemy.orm import Session


class DBAdaptor:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.item_repo = ItemRepository(db)
        self.category_repo = CategoryRepository(db)
        self.sub_category_repo = SubCategoryRepository(db)