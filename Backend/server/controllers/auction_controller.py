from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from server.middlewares.exception_handler import ExcRaiser400
from server.config import get_db
from server.schemas import (
    APIResponse, UpdateAuctionSchema,
    GetAuctionSchema, CreateAuctionSchema,
    PagedQuery, PagedResponse, AuctionQueryScalar,
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
    print(result)
    return APIResponse(status_code=201, data=result)


@route.get('/')
async def list(
    filter: AuctionQueryScalar = Depends(),
    db: Session = Depends(get_db)
) -> PagedResponse[list[GetAuctionSchema]]:
    result = await AuctionServices(db).list(filter)
    return result


@route.get('/{id}')
async def retrieve(
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


@route.delete('/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def delete(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
) -> APIResponse:
    result = await AuctionServices(db).delete(auction_id)
    return APIResponse(data={}) if result else\
    APIResponse(message='Fail', success=False)


@route.get('/finalize/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def finalize(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    auction = await AuctionServices(db).retrieve(auction_id)
    if auction.status != 'COMPLETED':
        return ExcRaiser400(
            detail='You can only finalize a completed auction'
        )
    result = await AuctionServices(db).finalize_payment(auction, user.id)
    return APIResponse(data=result)


@route.put('/set_inspecting/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def set_inspecting(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    result = await AuctionServices(db).set_inspecting(auction_id, user.id)
    return APIResponse(data=result)


# @route.put('/{auction_id}/participants')
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
