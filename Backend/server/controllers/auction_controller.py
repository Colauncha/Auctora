from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.middlewares.exception_handler import ExcRaiser400
from server.config import get_db
from server.schemas import (
    APIResponse, UpdateAuctionSchema,
    GetAuctionSchema, CreateAuctionSchema,
    RestartAuctionSchema, PagedResponse, AuctionQueryScalar,
)
from server.services import Services, current_user
from server.middlewares.auth import (
    permissions, Permissions,
    ServiceKeys
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
    result = await Services.auctionServices.create(db, data)
    print(result)
    return APIResponse(status_code=201, data=result)


@route.get('/')
async def list(
    filter: AuctionQueryScalar = Depends(),
    db: Session = Depends(get_db)
) -> PagedResponse[list[GetAuctionSchema]]:
    result = await Services.auctionServices.list(db, filter)
    return result


@route.get('/{id}')
async def retrieve(
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetAuctionSchema]:
    result = await Services.auctionServices.retrieve(db, id)
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
    result = await Services.auctionServices.update(db, auction_id, data)
    return APIResponse(data=result)


@route.delete('/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def delete(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
) -> APIResponse:
    result = await Services.auctionServices.delete(db, auction_id)
    return APIResponse(data={}) if result else\
    APIResponse(message='Fail', success=False)


@route.get('/finalize/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def finalize(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    auction = await Services.auctionServices.retrieve(db, auction_id)
    if auction.status != 'completed':
        return ExcRaiser400(
            detail='You can only finalize a completed auction'
        )
    result = await Services.auctionServices.finalize_payment(db, auction.id, user.id)
    return APIResponse(data=result)


@route.put('/set_inspecting/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def set_inspecting(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    auction = await Services.auctionServices.retrieve(db, auction_id)
    if auction.status != 'completed':
        return ExcRaiser400(
            detail='You can only inspect a completed auction'
        )
    result = await Services.auctionServices.set_inspecting(db, auction_id, user.id)
    return APIResponse(data=result)


@route.get('/refund/{auction_id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def refund(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    auction = await Services.auctionServices.retrieve(db, auction_id)
    if auction.status != 'completed':
        return ExcRaiser400(
            detail='You can only refund a completed auction'
        )
    result = await Services.auctionServices.refund(db, auction_id, user.id)
    return APIResponse(data=result)


@route.get('/complete_refund/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def refund_completed(
    user: current_user,
    auction_id: str,
    db: Session = Depends(get_db)
):
    result = await Services.auctionServices.complete_refund(db, auction_id, user.id)
    return APIResponse(data=result)


@route.patch('/restart/{auction_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.AUCTION)
async def restart(
    user: current_user,
    auction_id: str,
    data: RestartAuctionSchema,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    result = await Services.auctionServices.restart(db, auction_id, data)
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
