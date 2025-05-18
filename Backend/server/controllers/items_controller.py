from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser404
from server.config import get_db
from server.services.user_service import current_user
from server.middlewares.auth import permissions, Permissions
from server.services.item_service import ItemServices
from server.schemas import (
    APIResponse,
    CreateItemSchema, GetItemSchema,
    UpdateItemSchema
)
from server.enums import ServiceKeys
from server.enums.user_enums import UserRoles
from sqlalchemy.orm import Session


route = APIRouter(prefix='/items', tags=['Items'])


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
async def create(
    user: current_user,
    data: CreateItemSchema,
    db: Session = Depends(get_db) 
) -> APIResponse[GetItemSchema]:
    _data = CreateItemSchema.model_dump(data, exclude_unset=True)
    _data["users_id"] = user.id
    result = await ItemServices(db).create(_data)
    return APIResponse(data=result)


@route.get('/get_items')
@permissions(permission_level=Permissions.ALL)
async def get_items(
    user: current_user,
    db: Session = Depends(get_db)
):
    ...


@route.get('/')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def get_items(
    user: current_user,
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetItemSchema]:
    result = await ItemServices(db).retrieve(id)
    return APIResponse(data=result)


@route.put('/upload_images')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.ITEM)
async def upload_images(
    user: current_user,
    item_id: str,
    image1: Optional[UploadFile] = File(None),
    image2: Optional[UploadFile] = File(None),
    image3: Optional[UploadFile] = File(None),
    image4: Optional[UploadFile] = File(None),
    image5: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
) -> APIResponse[GetItemSchema]:
    
    item = await ItemServices(db).repo.get_by_attr({'id': item_id})

    images = [image1, image2, image3, image4, image5]
    content_type = ["image/jpeg", "image/png"]

    uploads = [
        image.file
        if image and image.content_type in content_type else None 
        for image in images
    ]

    result = await ItemServices(db).upload_images(item, uploads)
    return APIResponse(data=result)


@route.put('/{item_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.ITEM)
async def update(
    user: current_user,
    item_id: str,
    data: UpdateItemSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetItemSchema]:
    data = data.model_dump(exclude_unset=True, exclude_none=True)
    result = await ItemServices(db).update(item_id, data)
    return APIResponse(data=result)

# @route.get('/get_items')
# @permissions(permission_level=Permissions.ALL)
# async def get_items(
#     user: current_user,
#     db: Session = Depends(get_db)
# ):
#     ...