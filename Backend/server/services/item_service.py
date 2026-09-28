import asyncio
import cloudinary
import cloudinary.uploader
import inspect

from fastapi import UploadFile
from sqlalchemy.orm import Session

from server.config import cloudinary_init
from server.services.base_service import BaseService
from server.schemas import (
    GetItemSchema,
    ImageLinkObj
)
from server.middlewares.exception_handler import (
    ExcRaiser,
    ExcRaiser404,
    ExcRaiser500
)
from starlette.concurrency import run_in_threadpool


ALLOWED_IMAGE_TYPES = [
    "image/jpeg", "image/png", "image/webp",
    "image/bmp", "image/avif"
]


class ItemServices(BaseService):
    def __init__(self, item_repo, sub_cat_repo):
        self.repo = item_repo
        self.subcat_repo = sub_cat_repo

    async def create(self, data: dict[str, any]) -> GetItemSchema:
        try:
            category_ids = data.get("category_ids", [])
            sub_category_ids = data.get("sub_category_ids", [])

            for subcat_id in sub_category_ids:
                subcat = await self.subcat_repo.get_by_attr({"id": subcat_id})
                if not subcat or subcat.parent_id not in category_ids:
                    raise ExcRaiser(
                        status_code=400,
                        message="Invalid category",
                        detail=f"Subcategory '{subcat_id}' does not belong to any of the provided categories",
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
            result = await self.repo.get_by_attr({"id": id})
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

    async def upload_to_cloudinary(self, item_name: str, uploads: list) -> dict:
        """
        Uploads files to Cloudinary without touching the DB.
        `uploads` is positional (index 0 -> image_link, 1 -> image_link_2, ...);
        None entries are skipped. Returns {column_name: ImageLinkObj dict}.
        """
        folder_path = f"biddius/items/{item_name.strip().replace(' ', '_')}"

        async def _upload(content):
            _result = await run_in_threadpool(
                cloudinary.uploader.upload,
                content,
                folder=folder_path
            )
            result = {
                'link': _result.get('secure_url'),
                'public_id': _result.get('public_id')
            }
            return ImageLinkObj.model_validate(result).model_dump()

        slots = [
            ('image_link' if idx == 1 else f'image_link_{idx}', content)
            for idx, content in enumerate(uploads, 1)
            if content is not None
        ]
        results = await asyncio.gather(
            *(_upload(content) for _, content in slots),
            return_exceptions=True
        )

        links = {}
        errors = []
        for (column, _), res in zip(slots, results):
            if isinstance(res, BaseException):
                errors.append(res)
            else:
                links[column] = res

        if errors:
            # Don't leave partial uploads behind when any image fails
            await self.delete_from_cloudinary(
                [link['public_id'] for link in links.values()]
            )
            raise ExcRaiser(
                status_code=400,
                message='Unable to upload images',
                detail=repr(errors[0])
            )
        return links

    async def delete_from_cloudinary(self, public_ids: list[str]) -> None:
        """Best-effort removal of uploaded images, used for rollback."""
        for public_id in public_ids:
            if not public_id:
                continue
            try:
                await run_in_threadpool(cloudinary.uploader.destroy, public_id)
            except Exception as e:
                print(f"Failed to delete Cloudinary image {public_id}: {e}")

    async def upload_images(self, item, uploads: list[UploadFile]) -> GetItemSchema:
        try:
            cloudn_resp = await self.upload_to_cloudinary(item.name, uploads)
            updated_entity = await self.repo.update(item, cloudn_resp)
            return GetItemSchema.model_validate(*updated_entity)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    async def update(self, id: str, data: dict):
        try:
            entity = await self.repo.get_by_id(id)
            updated = await self.repo.update(entity, data)
            return GetItemSchema.model_validate(updated[0])
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))


# try:
#     ...
# except Exception as e:
#     if issubclass(type(e), ExcRaiser):
#         raise e
#     ...
