from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.config import app_configs, get_db, redis_store
from server.services import (
    get_auction_service,
    get_user_service,
    AuctionServices,
    UserServices
)
from server.schemas import (
    PagedQuery,
    PagedResponse,
    SearchQuery,
    GetAuctionSchema,
    GetUsersSchemaPublic
)


router = APIRouter(prefix='/landing', tags=['Landing Page'])


@router.get('/trending_auctions')
async def get_trending_auctions(
    db: Session = Depends(get_db),
    auctionServices: AuctionServices = Depends(get_auction_service)
):
    redis = await redis_store.get_async_redis()
    trending_auctions = await redis.get('trending_auctions')
    if trending_auctions:
        return PagedResponse.model_validate_json(trending_auctions)

    else:
        filter = PagedQuery(page=1, per_page=20)
        auctions = await auctionServices.list(
            db,
            filter,
            {'status': 'ACTIVE'}
        )
        await redis.set(
            'trending_auctions',
            auctions.model_dump_json(),
            ex=app_configs.REDIS_CACHE_EXPIRATION_LANDING
        )
        return auctions

@router.get('/search')
async def search(
    query: SearchQuery = Depends(),
    model: str = 'Auction',
    db: Session = Depends(get_db),
    userServices: UserServices = Depends(get_user_service),
    auctionServices: AuctionServices = Depends(get_auction_service)
) -> PagedResponse[list[Union[GetAuctionSchema, GetUsersSchemaPublic]]]:
    result = None
    if model == 'User':
        result = await userServices.search(db, query)
    elif model == 'Auction':
        result = await auctionServices.search(db, query)
    return result
