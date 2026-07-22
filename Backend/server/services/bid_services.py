from datetime import datetime
from server.utils.datetime_utils import now_utc
import json
from fastapi import WebSocket
from sqlalchemy.orm import Session
from server.services.base_service import BaseService
from server.config import app_configs
from server.enums.notification_enums import NotificationClasses
from server.config import redis_store
from server.models.bids import Bids
from server.middlewares.exception_handler import ExcRaiser400, ExcRaiser
from server.enums.auction_enums import AuctionStatus
from server.utils.ws_manager import WSManager
from server.events.publisher import publish_bid_placed, publish_outbid
from server.schemas import (
    CreateNotificationSchema,
    GetBidSchema, CreateBidSchema
)


class BidServices(BaseService):

    def __init__(
        self,
        bid_repo,
        user_repo,
        auction_repo,
        notif_service,
        auction_service,
        reward_service,
    ):
        self.repo = bid_repo
        self.user_repo = user_repo
        self.auction_repo = auction_repo
        self.notification = notif_service
        self.auctions_services = auction_service
        self.reward_service = reward_service

    async def retrieve(self, id: str) -> GetBidSchema:
        try:
            bid = await self.repo.get_by_id(id)
            return GetBidSchema.model_validate(bid)
        except Exception as e:
            raise e

    async def list(self, filter: dict) -> list[GetBidSchema]:
        try:
            bids = await self.repo.get_all(filter=filter)
            bids.data = [GetBidSchema.model_validate(bid) for bid in bids.data]
            return bids
        except Exception as e:
            raise e

    async def count(self, filter: dict) -> int:
        try:
            count = await self.repo.count(filter if filter else None)
            return count
        except Exception as e:
            raise e

    async def buy_now(self, data: CreateBidSchema) -> GetBidSchema:
        try:
            user = await self.user_repo.get_by_id(data.user_id)
            # Lock the auction row for the rest of this transaction so a
            # concurrent bid/buy_now on the same auction has to wait instead
            # of racing on current_price / buy_now.
            auction = await self.auction_repo.get_by_id(data.auction_id, for_update=True)
            date = now_utc()
            data.amount = auction.buy_now_price

            if auction.status != AuctionStatus.ACTIVE:
                raise ExcRaiser400(
                    f'Auction is not active, status: {auction.status.value}'
                )
            if auction.end_date < date:
                raise ExcRaiser400('Auction has ended')

            if auction.users_id == user.id:
                raise ExcRaiser400('You cannot bid on your own auction')

            if not auction.buy_now:
                raise ExcRaiser400('Buy now is not enabled')

            if auction.private:
                participant = await self.auction_repo.validate_participant(
                    data.auction_id, user.email
                )
                if not participant:
                    raise ExcRaiser(
                        status_code=403,
                        message='Unauthorized',
                        detail='You are not a participant in this auction'
                    )
            exist = await self.repo.exists(
                {"auction_id": data.auction_id, "user_id": data.user_id}
            )
            if exist:
                amount = data.amount - exist.amount
                e_amount = exist.amount
            else:
                amount = data.amount

            if user.available_balance < amount:
                raise ExcRaiser400('Insufficient wallet balance')
            if exist:
                bid = await self.repo.update(exist, {"amount": data.amount}, commit=False)
            else:
                bid = await self.repo.add(data.model_dump(), commit=False)
            await self.auction_repo.update(
                auction, {"current_price": data.amount}, commit=False
            )
            # Single commit releases the auction row lock together with
            # every write made under it.
            await self.repo.db.commit()

            if exist:
                await self.auctions_services.close(
                    id=data.auction_id,
                    caller="buy_now",
                    existing_amount=e_amount,
                )
            else:
                await self.auctions_services.close(
                    id=data.auction_id,
                    caller="buy_now",
                    existing_amount=0.0,
                )
            return bid
        except Exception as e:
            await self.repo.db.rollback()
            raise e

    async def create(self, data: CreateBidSchema) -> GetBidSchema:
        try:
            NOTIF_TITLE = 'Bid Placed'
            NOTIF_BODY = (
                "Bid submitted successfully in auction: "
                f"{data.auction_id}"
            )
            user = await self.user_repo.get_by_id(data.user_id)
            # Lock the auction row up front so two concurrent bids on the
            # same auction serialize instead of both reading the same
            # current_price and racing to write it back.
            auction = await self.auction_repo.get_by_id(data.auction_id, for_update=True)
            date = now_utc()

            if auction.status != AuctionStatus.ACTIVE:
                raise ExcRaiser400('Auction is not active')

            if auction.end_date < date:
                raise ExcRaiser400('Auction has ended')

            if auction.users_id == user.id:
                raise ExcRaiser400('You cannot bid on your own auction')

            # TODO: Check if price >= auction.buy_now_price
            if auction.buy_now:
                if data.amount >= auction.buy_now_price:
                    return await self.buy_now(data)

            # Check if price is within 10% of buy_now_price
            if auction.buy_now:
                if data.amount >= auction.buy_now_price * 0.9:
                    await self.auction_repo.update(
                        auction, {"buy_now": False}, commit=False
                    )

            prev_bids = sorted(
                auction.bids, key=lambda x: x.amount, reverse=True
            )

            if data.amount <= auction.current_price:
                raise ExcRaiser400(
                    'Amount must be higher than current highest bid'
                )

            if auction.private:
                participant = await self.auction_repo.validate_participant(
                    data.auction_id, user.email
                )
                if not participant:
                    raise ExcRaiser(
                        status_code=403,
                        message='Unauthorized',
                        detail='You are not a participant in this auction'
                    )

            # Check is user had placed a prev bid
            # If so, call update instead.
            exist = await self.repo.exists(
                {"auction_id": data.auction_id, "user_id": data.user_id}
            )
            if exist:
                return await self.update(exisiting_bid=exist, amount=data.amount)

            # Check available balance against bid amount (fast-path check;
            # wtab re-checks under lock since this read isn't locked)
            if user.available_balance < data.amount:
                raise ExcRaiser400('Insufficient wallet balance')

            # Move funds from users wallet to users auctioned_amount
            _ = await self.user_repo.wtab(user.id, data.amount, commit=False)
            bid = await self.repo.add(data.model_dump(), commit=False)
            await self.auction_repo.update(
                auction, {"current_price": data.amount}, commit=False
            )
            # Single commit releases the auction/user row locks together
            # with every write made under them.
            await self.repo.db.commit()

            if bid:
                await self.notify(
                    user.id,
                    NOTIF_TITLE,
                    NOTIF_BODY,
                    links=[f"{app_configs.FRONTEND_URL}/product-details/{auction.id}"],
                )
                await self.nphb(bid.auction_id, user.id)
                await publish_bid_placed({
                    "auction_id": data.auction_id,
                    "bid_user": user.id,
                    "amount": data.amount,
                    "link": f'{app_configs.FRONTEND_URL}/product-details/{auction.id}',
                    "email": user.email
                })
                # Reward user for placing a bid
                _ = await self.reward_service.save_reward_history(
                    user.id, reward_type="PLACE_BID"
                )
            return bid
        except Exception as e:
            await self.repo.db.rollback()
            raise e

    async def list_ws(
        self,
        auction_id: str,
    ):
        try:
            redis = await redis_store.get_async_redis()
            prev_bids = await self.list({"auction_id": auction_id})
            prev_bids = [
                {"id": str(b.user_id), "username": b.username, "amount": b.amount}
                for b in prev_bids.data
            ]
            prev_bids_ = json.dumps(prev_bids)
            _ = await redis.set(f"auction:{auction_id}", prev_bids_)
            return json.loads(prev_bids_)
        except Exception as e:
            raise e

    async def create_ws(
        self,
        data: CreateBidSchema,
        wsmanager: WSManager,
        ws: WebSocket,
    ):
        try:
            bid = await self.create(data)
            if bid:
                redis = await redis_store.get_async_redis()
                auction = await self.auction_repo.get_by_id(data.auction_id)
                prev_bids = sorted(
                    auction.bids, key=lambda x: x.amount, reverse=True
                )
                prev_bids = [
                        {
                            'id': str(pb.user_id),
                            'username': pb.username,
                            'amount': pb.amount
                        }
                        for pb in prev_bids
                    ]
                prev_bids_ = json.dumps(prev_bids)
                _ = await redis.set(f'auction:{auction.id}', prev_bids_)
                return prev_bids
            else:
                await wsmanager.send_message('Unable to place bid', ws)

        except Exception as e:
            print(e.__class__, e, e.__traceback__)
            await wsmanager.send_message(
                message=str(e),
                websocket=ws
            )

    async def add_watcher(self, auction_id: str, watcher: str):
        try:
            auction = await self.auction_repo.get_by_id(auction_id)
            if not auction:
                return False

            if auction.status in [
                AuctionStatus.COMPLETED,
                AuctionStatus.CANCLED,
            ]:
                return False
            watchers: list = auction.watchers or []

            if watcher in watchers:
                return True

            watchers.append(watcher)
            lent = len(watchers)
            await self.auction_repo.update(
                auction, {"watchers": watchers, "watchers_count": lent}
            )
            return True
        except Exception as e:
            raise e

    async def update(
        self,
        amount: float,
        user_id: str = None,
        auction_id: str = None,
        exisiting_bid: Bids = None,
    ) -> GetBidSchema:
        try:
            user__id = user_id if user_id else exisiting_bid.user_id
            auc__id = auction_id if auction_id else exisiting_bid.auction_id
            user = await self.user_repo.get_by_id(user__id)
            # Lock the auction row up front — same reasoning as create():
            # serialize concurrent writers instead of racing on current_price.
            auction = await self.auction_repo.get_by_id(auc__id, for_update=True)

            NOTIF_TITLE = 'Bid Placed'
            NOTIF_BODY = f'Bid submitted successfully in auction: {auc__id}'

            is_direct_update = False
            if exisiting_bid:
                amount_ = amount - exisiting_bid.amount

                if user.available_balance < amount_:
                    raise ExcRaiser400('Insufficient wallet balance')

                # Move funds from users wallet to users auctioned_amount
                _ = await self.user_repo.wtab(user.id, amount_, commit=False)
                bid = await self.repo.update(
                    exisiting_bid, {"amount": amount}, commit=False
                )
            elif user_id and auction_id:
                exists = await self.repo.exists(
                    {"auction_id": auction_id, "user_id": user_id}
                )
                if not exists:
                    raise ExcRaiser400(message='Bid not found')

                amount_ = amount - exists.amount

                if user.available_balance < amount_:
                    raise ExcRaiser400('Insufficient wallet balance')

                # Move funds from users wallet to users auctioned_amount
                _ = await self.user_repo.wtab(user.id, amount_, commit=False)
                bid = await self.repo.update(exists, {"amount": amount}, commit=False)
                is_direct_update = True
            else:
                raise ExcRaiser400(message='Bid not found')

            await self.auction_repo.update(
                auction, {"current_price": amount}, commit=False
            )
            # Single commit releases the auction/user row locks together
            # with every write made under them.
            await self.repo.db.commit()

            if bid and not is_direct_update:
                await self.notify(user.id, NOTIF_TITLE, NOTIF_BODY)
                await self.nphb(bid.auction_id, user.id)
            elif bid:
                await self.notify(
                    user.id,
                    NOTIF_TITLE,
                    NOTIF_BODY,
                    links=[
                        f"{app_configs.FRONTEND_URL}/product-details/{auction.id}"
                    ],
                )
                await self.nphb(bid.auction_id, user.id)
                await publish_bid_placed({
                    "auction_id": auc__id,
                    "bid_user": user.id,
                    "amount": amount,
                    "link": f'{app_configs.FRONTEND_URL}/product-details/{auc__id}',
                    "email": user.email
                })
            return bid
        except Exception as e:
            await self.repo.db.rollback()
            raise e

    async def delete(self, id: str):
        ...

    # Notifications
    async def notify(
        self,
        user_id: str,
        title: str,
        message: str,
        links: list = None,
    ):
        try:
            notice = CreateNotificationSchema(
                title=title, message=message,
                user_id=user_id, class_name=NotificationClasses.BID.value,
                links=links or []
            )
            await self.notification.create(notice)
        except Exception as e:
            raise e

    async def nphb(self, id: str, current_id: str):
        """nphb: NOTIFY PREVIOUS HIGHEST BIDDER"""
        try:
            NOTIF_TITLE = 'You Have been Outbid!'
            NOTIF_BODY = f'Someone placed a higher bid in auction: {id}'
            auction = await self.auction_repo.get_by_id(id)
            links = [f'{app_configs.FRONTEND_URL}/product-details/{auction.id}']

            # phb: previous highest bidder
            if len(auction.bids) <= 0:
                return
            bids = sorted(auction.bids, key=lambda x: x.amount, reverse=True)
            phb_bid = next((b for b in bids if b.user_id != current_id), None)
            if not phb_bid:
                return
            phb = phb_bid.user_id
            await self.notify(phb, NOTIF_TITLE, NOTIF_BODY, links=links)
            await publish_outbid(
                {
                    "auction_id": id,
                    "outbid_user": phb,
                    "link": f"{app_configs.FRONTEND_URL}/product-details/{auction.id}",
                    "email": (await self.user_repo.get_by_id(phb)).email,
                }
            )
        except Exception as e:
            raise e
