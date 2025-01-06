from sqlalchemy.orm import Session
from server.repositories import DBAdaptor
from server.models.items import Items
from server.schemas import (
    GetItemSchema, CreateItemSchema,
    UpdateItemSchema
)
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser404


class ItemServices:
    def __init__(self, db: Session):
        self.repo = DBAdaptor(db).item_repo
        self.subcat_repo = DBAdaptor(db).sub_category_repo

    async def create(self, data: dict[str, any]) -> GetItemSchema:
        try:
            subcat = await self.subcat_repo.get_by_attr(
                {'id': data.get('sub_category_id')}
            )
            if subcat.parent_id != data.get('category_id'):
                raise ExcRaiser(
                    status_code=400,
                    message="Invalid category",
                    detail="SUbcategory must be under Category"
                ) 
            item = await self.repo.add(data)
            print(item)
            if item:
                result = GetItemSchema.model_validate(item)
                return result
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser(

            )
        
    async def retrieve(self, id: str) -> GetItemSchema:
        try:
            result = await self.repo.get_by_attr({'id': id})
            if result:                
                return GetItemSchema.model_validate(result)
            raise ExcRaiser404(message='Item not found')
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser(
                message='Unable to fetch Item',
                status_code=400,
                detail=repr(e)
            )


# try:
#     ...
# except Exception as e:
#     if issubclass(type(e), ExcRaiser):
#         raise e
#     ...