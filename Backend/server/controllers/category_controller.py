from fastapi import APIRouter, Depends
from server.config import get_db
from server.enums.user_enums import Permissions
from server.middlewares.auth import permissions
from server.schemas import (
    CreateCategorySchema, CreateSubCategorySchema,
    GetCategorySchema, GetSubCategorySchema,
    APIResponse
)
from server.services.user_service import current_user
from server.services.category_service import CategoryServices
from sqlalchemy.orm import Session


route = APIRouter(prefix='/categories', tags=['categories'])
sub_route = APIRouter(prefix='/subcategories', tags=['subcategories'])


@route.post('/')
@permissions(permission_level=Permissions.ADMIN)
async def create_category(
    user: current_user,
    category: CreateCategorySchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetCategorySchema]:
    new_cat = await CategoryServices(db).create_category(category)
    return APIResponse(data=new_cat)


@route.get('/{id}')
async def get_category(
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetCategorySchema]:
    id = id.upper()
    category = await CategoryServices(db).get_cat_by_id(id)
    return APIResponse(data=category)


@route.get('/')
async def list_categories(
    db: Session = Depends(get_db)
) -> APIResponse[list[GetCategorySchema]]:
    categories = await CategoryServices(db).list_categories()
    return APIResponse(data=categories)


# Subcategory Routes
@sub_route.post('/')
@permissions(permission_level=Permissions.ADMIN)
async def create_sub_category(
    user: current_user,
    sub_cat: CreateSubCategorySchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetSubCategorySchema]:
    new_sub_cat = await CategoryServices(db).create_sub_category(sub_cat)
    return APIResponse(data=new_sub_cat)


@sub_route.get('/{id}')
async def get_sub_category(
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetSubCategorySchema]:
    id = id.upper()
    sub_category = await CategoryServices(db).get_subcat_by_id(id)
    return APIResponse(data=sub_category)


@sub_route.get('/')
async def list_sub_categories(
    db: Session = Depends(get_db)
) -> APIResponse[list[GetSubCategorySchema]]:
    sub_categories = await CategoryServices(db).list_sub_categories()
    return APIResponse(data=sub_categories)