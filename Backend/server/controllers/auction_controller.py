from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from server.config import get_db
from server.schemas import (
    APIResponse, UpdateAuctionSchema,
    GetAuctionSchema, CreateAuctionSchema,
    PagedQuery, PagedResponse,
)
from server.services.auction_service import AuctionServices
from server.middlewares.auth import (
    permissions, Permissions,
    current_user, ServiceKeys
)


route = APIRouter(prefix='/auctions', tags=['auction'])


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
async def create(
    user: current_user,
    data: CreateAuctionSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    data = data.model_dump(exclude_unset=True)
    data["users_id"] = user.id
    result = await AuctionServices(db).create(data)
    return APIResponse(status_code=201, data=result)


@route.get('/')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def list(
    user: current_user,
    filter: PagedQuery = Depends(PagedQuery),
    db: Session = Depends(get_db)
) -> PagedResponse[list[GetAuctionSchema]]:
    result = await AuctionServices(db).list(filter)
    return result


@route.get('/{id}')
@permissions(permission_level=Permissions.CLIENT)
async def retrieve(
    user: current_user,
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    result = await AuctionServices(db).retrieve(id)
    return APIResponse(data=result)


@route.put('/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def update(
    user: current_user,
    auction_id: str,
    data: UpdateAuctionSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    data = data.model_dump(exclude_unset=True)
    result = await AuctionServices(db).update(auction_id, data)
    return APIResponse(data=result)


# @route.delete('/{auction_id}')
# @permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
# async def delete(
#     user: current_user,
#     auction_id: str,
#     db: Session = Depends(get_db)
# ) -> APIResponse[GetAuctionSchema]:
#     result = await AuctionServices(db).delete(auction_id)
#     return APIResponse(data=result)


# @route.post('/{auction_id}/participants')
# @permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
# async def add_participant(
#     user: current_user,
#     auction_id: str,
#     email: list[str],   # This should be a list of emails
#     db: Session = Depends(get_db)
# ) -> APIResponse[GetAuctionSchema]:
#     result = await AuctionServices(db).add_participant(auction_id, email)
#     return APIResponse(data=result)


# @route.delete('/{auction_id}/participants')
# @permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
# async def remove_participant(
#     user: current_user,
#     auction_id: str,
#     email: list[str],   # This should be a list of emails
#     db: Session = Depends(get_db)
# ) -> APIResponse[GetAuctionSchema]:
#     result = await AuctionServices(db).remove_participant(auction_id, email)
#     return APIResponse(data=result)


@route.websocket('/ws_bids/{auction_id}')
@permissions(permission_level=Permissions.CLIENT)
async def ws_bid(
    user: current_user,
    auction_id: str,
    ws: WebSocket
):
    await ws.accept()
    await AuctionServices().ws_bids(auction_id, ws)
    await ws.close()