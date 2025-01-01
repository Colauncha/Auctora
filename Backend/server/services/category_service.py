from pydantic_core import PydanticSerializationError
from sqlalchemy.orm import Session
from server.repositories import DBAdaptor
from server.schemas import (
    CreateCategorySchema, GetCategorySchema,
    CreateSubCategorySchema, GetSubCategorySchema,
)
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser404


class CategoryServices:
    def __init__(self, db: Session):
        self.cat_repo = DBAdaptor(db).category_repo
        self.sub_cat_repo = DBAdaptor(db).sub_category_repo

    async def create_category(
            self, 
            category: CreateCategorySchema
        ) -> GetCategorySchema:
        try:
            category_dict = category.model_dump()
            _category = await self.cat_repo.add(category_dict)
            return _category
        except Exception as e:
            raise ExcRaiser(
                status_code=400,
                message="Unable to create category",
                detail=repr(e)
            )

    async def get_cat_by_id(self, id: str) -> GetCategorySchema:
        try:
            category = await self.cat_repo.get_by_attr({'id': id})
            if not category:
                raise ExcRaiser404("Category not found")
            valid_category = GetCategorySchema.model_validate(category)
            valid_category = valid_category.set_subcategories(
                [
                    {'name': sub.name, 'id': sub.id} 
                    for sub in category.sub_categories
                ]
            )
            return valid_category
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser(
                status_code=400,
                message="Unable to get category",
                detail=repr(e)
            )

    async def list_categories(self):
        try:
            categories = self.cat_repo.all()
            if not categories:
                raise ExcRaiser404("No categories found")
            valid_categories = [
                GetCategorySchema.model_validate(cat).set_subcategories(
                    [
                        {'name': sub.name, 'id': sub.id}
                        for sub in cat.sub_categories
                    ]
                )
                for cat in categories
            ]
            return valid_categories
        except Exception as e:
            raise ExcRaiser(
                status_code=400,
                message="Unable to get categories",
                detail=repr(e)
            )

    # Sub Category services
    async def create_sub_category(
            self,
            sub_cat: CreateSubCategorySchema
        ) -> GetSubCategorySchema:
        try:
            sub_category_dict = sub_cat.model_dump()
            sub_category = await self.sub_cat_repo.add(sub_category_dict)
            return sub_category
        except Exception as e:
            raise ExcRaiser(
                status_code=400,
                message="Unable to create subcategory",
                detail=repr(e)
            )

    async def get_subcat_by_id(self, id: str) -> GetSubCategorySchema:
        try:
            sub_category = await self.sub_cat_repo.get_by_attr({'id': id})
            if not sub_category:
                raise ExcRaiser404("Sub category not found")
            valid_sub_category = GetSubCategorySchema.model_validate(sub_category)
            valid_sub_category = valid_sub_category.set_parent_details(
                sub_category.parent.name,
                sub_category.parent.description
            )
            return valid_sub_category
        except Exception as e:
            print(e)
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser(
                status_code=400,
                message="Unable to get Sub category",
                detail=repr(e)
            )
        
    async def list_sub_categories(self):
        try:
            sub_categories = self.sub_cat_repo.all()
            if not sub_categories:
                raise ExcRaiser404("No sub categories found")
            valid_sub_categories = [
                GetSubCategorySchema.model_validate(sub_cat).set_parent_details(
                    sub_cat.parent.name,
                    sub_cat.parent.description
                )
                for sub_cat in sub_categories
            ]
            return valid_sub_categories
        except Exception as e:
            raise ExcRaiser(
                status_code=400,
                message="Unable to get sub categories",
                detail=repr(e)
            )