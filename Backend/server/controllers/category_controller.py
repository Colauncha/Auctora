from fastapi import APIRouter, Depends
from server.config import get_db
from server.enums.user_enums import Permissions
from server.middlewares.auth import permissions
from server.schemas import (
    CreateCategorySchema, CreateSubCategorySchema,
    GetCategorySchema, GetSubCategorySchema,
    APIResponse, UpdateCategorySchema,
    UpdateSubCategorySchema
)
from server.services.user_service import current_user
from server.services.category_service import CategoryServices
from sqlalchemy.orm import Session
from server.config import app_configs, get_db, redis_store
from server.utils.helpers import cache_obj_format, load_obj_from_cache
from server.middlewares.exception_handler import ExcRaiser500


route = APIRouter(prefix='/categories', tags=['categories'])
sub_route = APIRouter(prefix='/subcategories', tags=['subcategories'])


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
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
    redis = await redis_store.get_async_redis()
    category_cache = await redis.get('category_cache')
    if category_cache:
        try:
            loaded_cache = load_obj_from_cache(category_cache, GetCategorySchema)
            return APIResponse(data=loaded_cache)
        except Exception as e:
            raise ExcRaiser500(
                detail="Error loading category cache",
                exception=e
            )
    categories = await CategoryServices(db).list_categories()
    formated_categories = cache_obj_format(categories)
    await redis.set(
        'category_cache',
        formated_categories,
        ex=app_configs.REDIS_CACHE_EXPIRATION_CAT
    )
    return APIResponse(data=categories)


@route.put('/')
@permissions(permission_level=Permissions.ADMIN)
async def update(
    user: current_user,
    id: str,
    data: UpdateCategorySchema,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    response = await CategoryServices(db).update_category(id.upper(), data)
    return APIResponse(data=response)


# Subcategory Routes
@sub_route.post('/')
@permissions(permission_level=Permissions.CLIENT)
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

    redis = await redis_store.get_async_redis()
    sub_category_cache = await redis.get('sub_category_cache')
    if sub_category_cache:
        try:
            loaded_cache = load_obj_from_cache(sub_category_cache, GetSubCategorySchema)
            return APIResponse(data=loaded_cache)
        except Exception as e:
            raise ExcRaiser500(
                detail="Error loading subcategory cache",
                exception=e
            )
    sub_categories = await CategoryServices(db).list_sub_categories()

    formated_categories = cache_obj_format(sub_categories)
    await redis.set(
        'sub_category_cache',
        formated_categories,
        ex=app_configs.REDIS_CACHE_EXPIRATION_CAT
    )
    return APIResponse(data=sub_categories)


@sub_route.put('/')
@permissions(permission_level=Permissions.ADMIN)
async def update(
    user: current_user,
    id: str,
    data: UpdateSubCategorySchema,
    db: Session = Depends(get_db)
):
    response = await CategoryServices(db).update_sub_category(id.upper(), data)
    return APIResponse(data=response)