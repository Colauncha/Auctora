from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.config import app_configs, get_db
from server.services.auction_service import AuctionServices
from server.schemas import PagedQuery


router = APIRouter(prefix='/landing', tags=['Landing Page'])


@router.get('/trending_auctions')
async def get_trending_auctions(db: Session = Depends(get_db)):
    filter = PagedQuery(page=1, per_page=10)
    auctions = await AuctionServices(db).list(
        filter,
        {'status': 'ACTIVE'}
    )
    return auctions

@router.get('/search')
async def search(db: Session = Depends(get_db)):
    ...