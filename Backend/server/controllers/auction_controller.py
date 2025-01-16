from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.config import get_db
from server.schemas import (
    APIResponse,
    GetAuctionSchema, CreateAuctionSchema
)
from server.services.auction_service import AuctionServices
from server.middlewares.auth import permissions, Permissions, current_user


route = APIRouter(prefix='/auctions', tags=['auction'])


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
async def create(
    user: current_user,
    data: CreateAuctionSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    data = data.model_dump(exclude_unset=True)
    data["user_id"] = user.id
    result = await AuctionServices(db).create(data)
    return APIResponse(data=result)


@route.get('/')
async def list(
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    result = await AuctionServices(db).list()
    return APIResponse(data=result)


@route.get('/{id}')
@permissions(permission_level=Permissions.CLIENT)
async def retrieve(
    user: current_user,
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    result = await AuctionServices(db).retrieve(id)
    return APIResponse(data=result)