from datetime import datetime, timedelta
import inspect
from sqlalchemy.orm import Session
from fastapi import WebSocket

from server.config import redis_store, app_configs, notification_messages
from server.models.items import Items
from server.enums.notification_enums import NotificationClasses
from server.enums.auction_enums import AuctionStatus
from server.enums.payment_enums import PaymentStatus
from server.events import publisher as publ
from server.middlewares.exception_handler import (
    ExcRaiser,
    ExcRaiser404,
    ExcRaiser500,
    ExcRaiser400,
)
from server.utils.ex_inspect import ExtInspect
from server.schemas import (
    GetAuctionSchema,
    CreateNotificationSchema,
    CreateAuctionParticipantsSchema,
    PagedQuery,
    PagedResponse,
    CreatePaymentSchema,
    SearchQuery,
    GetPaymentSchema,
    RestartAuctionSchema,
)

from server.services.base_service import BaseService


class AuctionServices(BaseService):

    def __init__(
        self,
        auction_repo,
        auction_p_repo,
        user_repo,
        payment_repo,
        notif_service,
        chat_service,
        reward_service,
    ):
        self.repo = auction_repo
        self.participant_repo = auction_p_repo
        self.user_repo = user_repo
        self.payment_repo = payment_repo

        self.notification = notif_service
        self.chat_service = chat_service
        self.reward_service = reward_service

        self.debug = app_configs.DEBUG
        self.inspect = ExtInspect(self.__class__.__name__).info

    # Auction services
    async def create(self, data: dict):
        try:
            NOTIF_TITLE = "New Auction"
            NOTIF_BODY = "Your new auction has been created"
            NOTIF_BODY_PRIV = (
                "Your new private auction has been created "
                "and the participants have been notified"
            )
            participants: dict = data.pop('participants')
            item: dict = data.pop('item')
            user_id = data.get('users_id')
            item['users_id'] = user_id
            data['item'] = [Items(**item)]
            data['status'] = AuctionStatus(data.get('status'))
            result = await self.repo.add(data)
            if result.private == True:
                for p in participants:
                    await self.create_participants(
                        {"auction_id": result.id, "participant_email": p},
                        auction=GetAuctionSchema.model_validate(result),
                    )
            await self.notify(
                user_id,
                NOTIF_TITLE,
                NOTIF_BODY_PRIV if result.private else NOTIF_BODY,
                links=[f"{app_configs.FRONTEND_URL}/product-details/{result.id}"],
                class_name=NotificationClasses.AUCTION.value,
            )
            await publ.publish_create_auction(
                {
                    'email': data.get('users_email'),
                    'link': f'{app_configs.FRONTEND_URL}/product-details/{result.id}',
                    'auction': result,
                    'item': item,
                    'item_image': item.get('image_link').get('link') if item.get('image_link') else None,
                }
            )
            # Reward user for listing product
            _ = await self.reward_service.save_reward_history(
                user_id, reward_type="LIST_PRODUCT"
            )
            return GetAuctionSchema.model_validate(result)
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def retrieve(self, id: str):
        try:
            result = await self.repo.get_by_id(id)
            # print(result.chat)
            if not result:
                raise ExcRaiser404("Auction not found")
            return GetAuctionSchema.model_validate(result)
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                self.inspect()
                raise ExcRaiser500(detail=str(e))
            raise ExcRaiser500(detail=str(e))

    async def list(
        self, filter: PagedQuery, extra: dict = None
    ) -> PagedResponse[list[GetAuctionSchema]]:
        try:
            filter = filter.model_dump(exclude_unset=True, exclude_none=True)
            filter['private'] = False
            if extra:
                filter.update(extra)
            print(filter)
            result = await self.repo.get_all(filter)
            result.data = [GetAuctionSchema.model_validate(r) for r in result.data]
            return result
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def count(self) -> int:
        try:
            count = await self.repo.count()
            return count
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def update(self, id: str, data: dict):
        try:
            entity = await self.repo.get_by_id(id)
            updated = await self.repo.update(entity, data)
            return GetAuctionSchema.model_validate(updated[0])
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    # Auction participants
    async def create_participants(
        self, data: CreateAuctionParticipantsSchema, auction: dict = None
    ):
        try:
            NOTIF_TITLE = 'Auction Invitation'
            NOTIF_BODY = (
                "You have been invited to participate in an auction. "
                f"Auction ID: {data.get('auction_id')}"
            )
            user = await self.user_repo.get_by_email(data.get("participant_email"))
            _ = await self.participant_repo.add(data)
            if user:
                await self.notify(
                    str(user.id),
                    NOTIF_TITLE,
                    NOTIF_BODY,
                    links=[
                        f'{app_configs.FRONTEND_URL}/product-details/{data.get("auction_id")}'
                    ],
                    class_name=NotificationClasses.AUCTION.value,
                )
            auct = auction.model_dump() if auction else None
            item = auction.item[0].model_dump() if auction and auction.item else None
            image_link = item.get('image_link').get('link') if item and item.get('image_link') else None
            await publ.publish_create_auction(
                {
                    'email': data.get('participant_email'),
                    'link': f'{app_configs.FRONTEND_URL}/product-details/{data.get("auction_id")}',
                    'auction': auct,
                    'sign_up_link': f'{app_configs.FRONTEND_URL}/sign-up',
                    'item': item,
                    'item_image': image_link
                }
            )
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def ws_bids(self, auction_id: str, ws: WebSocket):
        try:
            async_redis = await redis_store.get_async_redis()
            bid_list = async_redis.get(f'auction:{auction_id}')
            await ws.send(bid_list)
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def close(
        self,
        id: str,
        db: Session = None,
        caller: str = "create",
        existing_amount: float = 0.0,
    ):
        try:
            # Get the auction, bids and winner's details
            auction = await self.repo.attachDB(db).get_by_id(id)
            bids: list = auction.bids
            winner = None
            if len(bids) > 0:
                winner = max(bids, key=lambda x: x.amount)

            # If auction exists
            if auction:
                # check if price >= reserve price else cancel auction
                if auction.use_reserve_price and\
                    auction.reserve_price >= winner.amount:
                    await self.repo.update(auction, {"status": AuctionStatus.CANCLED})
                    await self.notify(
                        auction.users_id,
                        "Auction Closed",
                        "Your auction has been closed",
                    )
                    for bid in bids:
                        _ = await self.user_repo.attachDB(db).abtw(bid.user_id, bid.amount)
                        await self.notify(
                            bid.user_id,
                            "Auction Lost",
                            "You have lost the auction, Amount has been returned",
                            class_name=NotificationClasses.AUCTION.value,
                        )
                        return

                # Update auction status to completed
                await self.repo.update(auction, {"status": AuctionStatus.COMPLETED})
                await self.notify(
                    auction.users_id, "Auction Closed", "Your auction has been closed"
                )
                await self.payment_repo.attachDB(db).add(
                    CreatePaymentSchema(
                        from_id=winner.user_id,
                        to_id=auction.users_id,
                        auction_id=auction.id,
                        amount=winner.amount,
                        due_data=datetime.now().astimezone()
                        + timedelta(minutes=app_configs.PAYMENT_DUE_DAYS),
                    ),
                    caller=caller,
                    existing_amount=existing_amount,
                )
                await self.notify(
                    winner.user_id,
                    "Auction Won",
                    "Congratulations, you have won the auction",
                    links=[f"{app_configs.FRONTEND_URL}/product/finalize/{id}"],
                    class_name=NotificationClasses.AUCTION.value,
                )
                await publ.publish_win_auction(
                    {
                        'auction_id': id,
                        'winner': winner.user_id,
                        'user': winner.user,
                        'email': winner.user.email,
                        'amount': winner.amount,
                        'link': f'{app_configs.FRONTEND_URL}/product/finalize/{id}'
                    }
                )
                await self.chat_service.create_chat(
                    {
                        'auctions_id': auction.id,
                        'buyer_id': winner.user_id,
                        'seller_id': auction.users_id,
                        'conversation': []
                    }
                )
                # Reward winner for winning auction
                _ = await self.reward_service.save_reward_history(
                    winner.user_id, reward_type="WIN_AUCTION"
                )
                # TODO: Develop system to move amount to company's account
                bids = sorted(bids, key=lambda x: x.amount)
                bids = bids[:-1]
                for bid in bids:
                    _ = await self.user_repo.abtw(bid.user_id, bid.amount)
                    await self.notify(
                        bid.user_id,
                        "Auction Lost",
                        "You have lost the auction, Amount has been returned",
                        class_name=NotificationClasses.AUCTION.value,
                        links=[
                            f"{app_configs.FRONTEND_URL}/product-details/{auction.id}"
                        ],
                    )
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def restart(self, id: str, data: RestartAuctionSchema):
        try:
            auction = await self.repo.get_by_id(id)
            payment = await self.payment_repo.get_by_attr({"auction_id": id})
            restart_status = [
                AuctionStatus.COMPLETED,
                AuctionStatus.CANCLED
            ]
            if not auction:
                raise ExcRaiser404("Auction not found")
            if auction.status not in restart_status:
                raise ExcRaiser400("Auction is not completed or canceled")
            if not payment or (payment.status == PaymentStatus.REFUNDED):
                # Reset the auction status to PENDING
                auction.start_date = data.start_date or auction.start_date
                auction.end_date = data.end_date
                auction.start_price = data.start_price or auction.start_price
                auction.buy_now = data.buy_now if data.buy_now is not None else auction.buy_now
                auction.buy_now_price = data.buy_now_price or auction.buy_now_price
                auction.status = AuctionStatus.PENDING
                auction.bids = []

                if payment:
                    # If payment exists, delete it
                    await self.payment_repo.delete(payment)
                # Notify the seller and participants
                await self.notify(
                    auction.users_id,
                    "Auction Restarted",
                    notification_messages.AUCTION_RESTARTED.message,
                    links=[
                        f"{notification_messages.AUCTION_RESTARTED.link[0]}{id}",
                    ],
                    class_name=NotificationClasses.AUCTION.value,
                )
            else:
                raise ExcRaiser400(
                    detail='Payment completed or not refunded, cannot restart auction'
                )
            return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def set_inspecting(self, id: str, buyer_id: str):
        try:
            payment = await self.payment_repo.get_by_attr({"auction_id": id})
            payment = GetPaymentSchema.model_validate(payment)
            if payment:
                if payment.status != 'pending':
                    raise ExcRaiser400(
                        detail='Payment has already been processed'
                    )
                if payment.from_id != buyer_id:
                    raise ExcRaiser400(
                        detail='You are not the buyer of this auction'
                    )

                await self.payment_repo.update(
                    payment,
                    {
                        "status": PaymentStatus.INSPECTING,
                        "due_data": datetime.now().astimezone() + timedelta(days=5),
                    },
                )
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def finalize_payment(self, auction_id, buyer_id: str, db: Session = None):
        try:
            payment = await self.payment_repo.attachDB(db).get_by_attr(
                {"auction_id": auction_id}
            )

            if not payment:
                raise ExcRaiser400(
                    detail='Entity not found'
                )
            payment = GetPaymentSchema.model_validate(payment)
            if payment.from_id != buyer_id:
                raise ExcRaiser400(
                    detail='You are not the buyer of this auction'
                )
            res = await self.payment_repo.disburse(payment)
            if res:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def refund(self, id: str, buyer_id: str):
        try:
            payment = await self.payment_repo.get_by_attr({"auction_id": id})
            payment_ = GetPaymentSchema.model_validate(payment)
            if payment_.from_id != buyer_id:
                raise ExcRaiser400(
                    detail='You are not the buyer of this auction'
                )
            blocked_status = [
                PaymentStatus.REFUNDING.value,
                PaymentStatus.REFUNDED.value,
                PaymentStatus.COMPLETED.value
            ]
            if payment_.status in blocked_status:
                raise ExcRaiser400(
                    detail='Payment is already in process or completed'
                )
            payment_.status = PaymentStatus.REFUNDING
            payment_.due_data = datetime.now().astimezone() + timedelta(minutes=0.0)
            payment_.refund_requested = True
            payment_.seller_refund_confirmed = False
            payment_ = payment_.model_dump(
                exclude_none=True,
                exclude_unset=True,
                exclude={'buyer', 'seller'}
            )

            # Update the payment status to REFUNDING
            res = await self.payment_repo.update(payment, payment_)

            # Notify the seller and buyer
            await self.notify(
                payment.to_id,
                "Refund Requested",
                notification_messages.REFUND_REQUEST_SELLER.message,
                links=[
                    f"{notification_messages.REFUND_REQUEST_SELLER.link}{id}",
                ],
                class_name=NotificationClasses.PAYMENT.value,
            )

            # Notify the buyer that the refund is being processed
            await self.notify(
                payment.from_id,
                "Refund Processing",
                notification_messages.REFUND_REQUEST_BUYER.message,
                class_name=NotificationClasses.PAYMENT.value,
            )

            if res:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def complete_refund(self, id: str, seller_id: str):
        try:
            payment = await self.payment_repo.get_by_attr({"auction_id": id})
            payment_ = GetPaymentSchema.model_validate(payment)
            if payment_.to_id != seller_id:
                raise ExcRaiser400(
                    detail='You are not the creator of this auction'
                )
            blocked_status = [
                PaymentStatus.INSPECTING.value,
                PaymentStatus.PENDING.value,
                PaymentStatus.REFUNDED.value,
                PaymentStatus.COMPLETED.value
            ]
            if payment_.status in blocked_status:
                raise ExcRaiser400(
                    detail='Payment is not up for a refund'
                )

            # Update the payment status to REFUNDING
            res = await self.payment_repo.refund(payment_)

            # Notify the seller and buyer
            await self.notify(
                payment.to_id,
                "Refund Requested",
                notification_messages.REFUND_COMPLETED,
                links=[
                    f"{notification_messages.REFUND_COMPLETED.link[0]}{id}",
                ],
                class_name=NotificationClasses.PAYMENT.value,
            )

            # Notify the buyer that the refund is being processed
            await self.notify(
                payment.from_id,
                "Refund Processing",
                notification_messages.REFUND_COMPLETED,
                links=[
                    f"{notification_messages.REFUND_COMPLETED.link[1]}{id}",
                ],
                class_name=NotificationClasses.PAYMENT.value,
            )

            if res:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def delete(self, id: str):
        try:
            auction = await self.repo.get_by_id(id)
            bids = auction.bids
            for bid in bids:
                _ = await self.user_repo.abtw(bid.user_id, bid.amount)
                await self.notify(
                    bid.user_id,
                    "Auction Closed",
                    "The auction has been canceled, The amount placed on the bid has been returned",
                )
            result = await self.repo.delete(auction)
            if result:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    # Notifications
    async def notify(
        self,
        user_id: str,
        title: str,
        message: str,
        links: list = None,
        class_name: str = None,
    ):
        try:
            notice = CreateNotificationSchema(
                title=title, message=message,
                user_id=user_id, links=links or [],
                class_name=class_name
            )
            await self.notification.create(notice)
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def search(
        self,
        filter: SearchQuery,
    ) -> PagedResponse:
        try:
            filter = filter.model_dump()
            result = await self.repo.search(filter)
            result.data = [GetAuctionSchema.model_validate(r) for r in result.data]
            return result
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
