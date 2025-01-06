from fastapi import APIRouter, Depends
from server.config import get_db
from server.services.user_service import current_user
from server.middlewares.auth import permissions, Permissions
from server.services.item_service import ItemServices
from server.schemas import (
    APIResponse,
    CreateItemSchema, GetItemSchema,
    UpdateItemSchema
)
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
    _data["sellers_id"] = user.id
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


# @route.get('/get_items')
# @permissions(permission_level=Permissions.ALL)
# async def get_items(
#     user: current_user,
#     db: Session = Depends(get_db)
# ):
#     ...