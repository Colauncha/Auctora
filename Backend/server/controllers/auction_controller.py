from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.config import get_db
from server.schemas import (
    APIResponse,
    GetAuctionSchema, CreateAuctionSchema
)
from server.services.auction_service import AuctionServices
from server.middlewares.auth import permissions, Permissions, current_user


route = APIRouter(prefix='/auction', tags=['auction'])


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
async def create(
    user: current_user,
    data: CreateAuctionSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    data = data.model_dump(exclude_unset=True)
    data.user_id = user.id
    result = AuctionServices(db).create(data)
    return APIResponse(data=result)