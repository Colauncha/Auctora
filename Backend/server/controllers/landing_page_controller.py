import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.config import app_configs, get_db, redis_store
from server.services.auction_service import AuctionServices
from server.schemas import PagedQuery


router = APIRouter(prefix='/landing', tags=['Landing Page'])


@router.get('/trending_auctions')
async def get_trending_auctions(db: Session = Depends(get_db)):
    redis = await redis_store.get_async_redis()
    trending_auctions = await redis.get('trending_auctions')
    if trending_auctions:
        return json.loads(trending_auctions)
    # If not in Redis, fetch from DB
    else:
        filter = PagedQuery(page=1, per_page=10)
        auctions = await AuctionServices(db).list(
            filter,
            {'status': 'ACTIVE'}
        )
        # Store in Redis for future requests
        await redis.set(
            'trending_auctions',
            json.dumps(auctions),
            ex=app_configs.REDIS_CACHE_EXPIRATION_LANDING
        )
        return auctions

@router.get('/search')
async def search(db: Session = Depends(get_db)):
    ...