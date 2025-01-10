import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from sqlalchemy.orm import Session
from server.config import cloudinary_init
from server.repositories import DBAdaptor
from server.models.items import Items
from server.schemas import (
    GetItemSchema, CreateItemSchema,
    UpdateItemSchema, ImageLinkObj
)
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser404
from starlette.concurrency import run_in_threadpool


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
                    detail="Subcategory must be under Category"
                ) 
            item = await self.repo.add(data)
            if item:
                result = GetItemSchema.model_validate(item)
                return result
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser(
                message='Unable to create Item',
                status_code=400,
                detail=repr(e)
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

    async def upload_images(
            self, item, uploads: list[UploadFile]
        ) -> GetItemSchema:
        try:
            cloudn_resp = {}
            for idx, content in enumerate(uploads, 1):
                if content is None:
                    continue
                _result = await run_in_threadpool(cloudinary.uploader.upload, content)
                result = {
                    'link': _result.get('secure_url'),
                    'public_id': _result.get('public_id')
                }
                result = ImageLinkObj.model_validate(result).model_dump()
                cloudn_resp['image_link' if idx == 1 else f'image_link_{idx}'] = result
            updated_entity = await self.repo.update(item, cloudn_resp)
            return GetItemSchema.model_validate(*updated_entity)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

# try:
#     ...
# except Exception as e:
#     if issubclass(type(e), ExcRaiser):
#         raise e
#     ...