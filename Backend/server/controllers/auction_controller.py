from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.middlewares.exception_handler import ExcRaiser400
from server.config import get_db
from server.schemas import (
    APIResponse, UpdateAuctionSchema,
    GetAuctionSchema, CreateAuctionSchema,
    RestartAuctionSchema, PagedResponse, AuctionQueryScalar,
)
from server.services import current_user, AuctionServices, get_auction_service
from server.middlewares.auth import (
    RequirePermission, permissions, Permissions,
    ServiceKeys
)


route = APIRouter(prefix='/auctions', tags=['auction'])


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
async def create(
    user: current_user,
    data: CreateAuctionSchema,
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> APIResponse[GetAuctionSchema]:
    data = data.model_dump(exclude_unset=True)
    data["users_id"] = user.id
    result = await auctionServices.create(data)
    return APIResponse(status_code=201, data=result)


@route.get('/')
async def list(
    filter: AuctionQueryScalar = Depends(),
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> PagedResponse[list[GetAuctionSchema]]:
    result = await auctionServices.list(filter)
    return result


@route.get('/{id}')
async def retrieve(
    id: str, auctionServices: AuctionServices = Depends(get_auction_service)
) -> APIResponse[GetAuctionSchema]:
    result = await auctionServices.retrieve(id)
    return APIResponse(data=result)


@route.put('/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def update(
    user: current_user,
    auction_id: str,
    data: UpdateAuctionSchema,
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> APIResponse[GetAuctionSchema]:
    data = data.model_dump(exclude_unset=True)
    result = await auctionServices.update(auction_id, data)
    return APIResponse(data=result)


@route.delete('/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def delete(
    user: current_user,
    auction_id: str,
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> APIResponse:
    result = await auctionServices.delete(auction_id)
    return APIResponse(data={}) if result else\
    APIResponse(message='Fail', success=False)


@route.get('/finalize/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def finalize(
    user: current_user,
    auction_id: str,
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> APIResponse[bool]:
    auction = await auctionServices.retrieve(auction_id)
    if auction.status != 'completed':
        return ExcRaiser400(
            detail='You can only finalize a completed auction'
        )
    result = await auctionServices.finalize_payment(auction.id, user.id)
    return APIResponse(data=result)


@route.put('/set_inspecting/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def set_inspecting(
    user: current_user,
    auction_id: str,
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> APIResponse[bool]:
    auction = await auctionServices.retrieve(auction_id)
    if auction.status != 'completed':
        return ExcRaiser400(
            detail='You can only inspect a completed auction'
        )
    result = await auctionServices.set_inspecting(auction_id, user.id)
    return APIResponse(data=result)


@route.get('/refund/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def refund(
    user: current_user,
    auction_id: str,
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> APIResponse[bool]:
    auction = await auctionServices.retrieve(auction_id)
    if auction.status != 'completed':
        return ExcRaiser400(
            detail='You can only refund a completed auction'
        )
    result = await auctionServices.refund(auction_id, user.id)
    return APIResponse(data=result)


@route.get('/complete_refund/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def refund_completed(
    user: current_user,
    auction_id: str,
    auctionServices: AuctionServices = Depends(get_auction_service),
):
    result = await auctionServices.complete_refund(auction_id, user.id)
    return APIResponse(data=result)


@route.patch('/restart/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def restart(
    user: current_user,
    auction_id: str,
    data: RestartAuctionSchema,
    auctionServices: AuctionServices = Depends(get_auction_service),
) -> APIResponse[bool]:
    result = await auctionServices.restart(auction_id, data)
    return APIResponse(data=result)


@route.get('/stats/count')
@permissions(permission_level=Permissions.ADMIN)
async def count_auctions(
    user: current_user, auctionServices: AuctionServices = Depends(get_auction_service)
) -> APIResponse[dict[str, int]]:
    result = await auctionServices.count()
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
