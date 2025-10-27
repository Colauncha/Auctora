import math

from sqlalchemy import String

from server.models.auction import Auctions, AuctionParticipants
from server.models.items import Items
from server.repositories.repository import Repository, no_db_error
from server.enums.auction_enums import AuctionStatus
from server.schemas import PagedResponse
from server.utils import paginator


class AuctionParticipantRepository(Repository):
    def __init__(self):
        super().__init__(AuctionParticipants)


class AuctionRepository(Repository):
    def __init__(self, auction_participant: AuctionParticipantRepository):
        super().__init__(Auctions)
        self.auction_P = auction_participant

    async def validate_participant(self, auction_id: str, participant: str):
        try:
            id = f'{auction_id}:{participant}'
            confirmed_participant = await self.auction_P.get_by_id(id)
            return True if confirmed_participant else False
        except Exception as e:
            raise e

    @staticmethod
    def queryToFloatList(input: str):
        if not input:
            return None
        float_list = input.split('-')
        if len(float_list) > 2 or len(float_list) < 1:
            return None
        if len(float_list) == 1:
            return [0.00, float(float_list[0])]
        float_list = [float(figure) for figure in float_list]
        return float_list

    @no_db_error
    async def get_all(
        self,
        filter_ = None,
        relative = False,
        sort = 'watchers_count'
    ):
        filter_ = filter_.copy() if filter_ else {}

        page = filter_.pop('page', 1)
        per_page = filter_.pop('per_page', 10)
        cat_id = filter_.pop('category_id', None)
        subcat_id = filter_.pop('sub_category_id', None)

        start_price = self.queryToFloatList(filter_.pop('start_price', None))
        current_price = self.queryToFloatList(filter_.pop('current_price', None))
        buy_now_price = self.queryToFloatList(filter_.pop('buy_now_price', None))

        limit = per_page
        offset = paginator(page, per_page)
        QueryModel: Auctions = Auctions

        try:
            query = self.db.query(QueryModel)

            for key, value in filter_.items():
                if hasattr(QueryModel, key):
                    query = query.filter(getattr(QueryModel, key) == value)

            if hasattr(QueryModel, sort):
                query = query.order_by(getattr(QueryModel, sort).desc())

            if cat_id:
                query = query.filter(QueryModel.item.any(category_id=cat_id))
            if subcat_id:
                query = query.filter(QueryModel.item.any(subcat_id=subcat_id))

            if start_price:
                query = query.filter(
                    QueryModel.start_price >= start_price[0],
                    QueryModel.start_price <= start_price[1]
                )
            if current_price:
                query = query.filter(
                    QueryModel.current_price >= current_price[0],
                    QueryModel.current_price <= current_price[1]
                )
            if buy_now_price:
                query = query.filter(
                    QueryModel.buy_now_price >= buy_now_price[0],
                    QueryModel.buy_now_price <= buy_now_price[1]
                )

            total = query.count()
            query = query.limit(limit).offset(offset)
            results = query.all()
        except Exception as e:
            print(f"Error in get_all: {e}")
            raise e
        count = len(results)
        pages = max(math.ceil(total / limit), 1)
        return PagedResponse(
            data=results,
            pages=pages,
            page_number=page,
            per_page=limit,
            count=count,
            total=total,
        )

    @no_db_error
    async def search(self, filter_: dict | None = None):
        filter_ = filter_.copy() if filter_ else {}
        page = filter_.pop("page", 1)
        per_page = filter_.pop("per_page", 10)

        limit = per_page
        offset = paginator(page, per_page)
        QueryModel = Auctions

        try:
            search_term = filter_.get("q", "").strip()
            query = self.db.query(QueryModel)

            if search_term:
                query = query.filter(
                    QueryModel.item.any(
                        (Items.name.ilike(f"%{search_term}%")) |
                        (Items.description.ilike(f"%{search_term}%"))
                    )
                )

            total = query.count()
            results = query.limit(limit).offset(offset).all()

        except Exception as e:
            print(f"[Search Error] {e}")
            raise

        pages = max(math.ceil(total / limit), 1)
        return PagedResponse(
            data=results,
            pages=pages,
            page_number=page,
            per_page=limit,
            count=len(results),
            total=total,
        )

    @no_db_error
    async def count(self) -> dict[str, int]:
        try:
            total = self.db.query(self._Model).count()
            if total == 0:
                return {
                    'total': 0, 'active': 0, 'completed': 0,
                    'cancelled': 0, 'pending': 0, 'private': 0
                }
            active = self.db.query(self._Model).filter_by(status=AuctionStatus.ACTIVE).count()
            completed = self.db.query(self._Model).filter_by(status=AuctionStatus.COMPLETED).count()
            cancelled = self.db.query(self._Model).filter_by(status=AuctionStatus.CANCLED).count()
            pending = self.db.query(self._Model).filter_by(status=AuctionStatus.PENDING).count()
            private = self.db.query(self._Model).filter_by(private=True).count()
            return {
                'total': total,
                'active': active,
                'completed': completed,
                'cancelled': cancelled,
                'pending': pending,
                'private': private
            }
        except Exception as e:
            print(f"Error in count: {e}")
            raise e
