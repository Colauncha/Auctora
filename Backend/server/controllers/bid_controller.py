from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.config import get_db
from server.middlewares.auth import (
    permissions, Permissions,
    current_user, ServiceKeys
)
from server.schemas import (
    CreateBidSchema, GetBidSchema, UpdateBidSchema,
    APIResponse, BidQuery, PagedResponse
)
from server.services.bid_services import BidServices


route = APIRouter(prefix='/bids', tags=['bids'])


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
async def create(
    user: current_user,
    data: CreateBidSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetBidSchema]:
    data = data.model_dump()
    data["user_id"] = user.id
    data["username"] = user.username
    result = await BidServices(db).create(CreateBidSchema(**data))
    return result


@route.put('/{bid_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.BID)
async def update(
    user: current_user,
    bid_id: str,
    amount: UpdateBidSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetBidSchema]:
    existing_bid = await BidServices(db).retrieve(bid_id)
    result = await BidServices(db).update(
        amount.amount, exisiting_bid=existing_bid
    )
    return result


@route.get('/')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def list(
    user: current_user,
    query: BidQuery = Depends(BidQuery),
    db: Session = Depends(get_db)
) -> PagedResponse:
    result = await BidServices(db).list(query.model_dump(exclude_unset=True))
    return result


@route.get('/{id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def retrieve(
    user: current_user,
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetBidSchema]:
    result = await BidServices(db).retrieve(id)
    return result