from datetime import datetime, timedelta
import inspect
from sqlalchemy.orm import Session
from fastapi import WebSocket

from server.config import redis_store, app_configs, notification_messages
from server.models.items import Items
from server.enums.notification_enums import NotificationClasses
from server.enums.auction_enums import AuctionStatus
from server.enums.payment_enums import PaymentStatus
from server.events.publisher import publish_win_auction
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404, ExcRaiser500, ExcRaiser400
)
from server.schemas import (
    GetAuctionSchema,
    CreateNotificationSchema, CreateAuctionParticipantsSchema,
    PagedQuery, PagedResponse, CreatePaymentSchema,
    SearchQuery, GetPaymentSchema, RestartAuctionSchema
)


class AuctionServices:
    def __init__(
        self, auction_repo, auction_p_repo,
        user_repo, payment_repo, notif_service
    ):
        self.repo = auction_repo
        self.participant_repo = auction_p_repo
        self.user_repo = user_repo
        self.notification = notif_service
        self.payment_repo = payment_repo
        self.debug = app_configs.DEBUG

    # Auction services
    async def create(self, db: Session, data: dict):
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
            result = await self.repo.attachDB(db).add(data)
            if result.private == True:
                for p in participants:
                    await self.create_participants(
                        db, {'auction_id': result.id, 'participant_email': p}
                    )
            await self.notify(
                db, user_id, NOTIF_TITLE,
                NOTIF_BODY_PRIV if result.private else NOTIF_BODY
            )
            return GetAuctionSchema.model_validate(result)
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def retrieve(self, db: Session, id: str):
        try:
            result = await self.repo.attachDB(db).get_by_id(id)
            if not result:
                raise ExcRaiser404("Auction not found")
            return GetAuctionSchema.model_validate(result)
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def list(
            self,
            db: Session,
            filter: PagedQuery,
            extra: dict = None
        ) -> PagedResponse[list[GetAuctionSchema]]:
        try:
            filter = filter.model_dump(exclude_unset=True, exclude_none=True)
            filter['private'] = False
            if extra:
                filter.update(extra)
            print(filter)
            result = await self.repo.attachDB(db).get_all(filter)
            result.data = [GetAuctionSchema.model_validate(r) for r in result.data]
            return result
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def update(self, db: Session, id: str, data: dict):
        try:
            entity = await self.repo.attachDB(db).get_by_id(id)
            updated = await self.repo.attachDB(db).update(entity, data)
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
            self,
            db: Session,
            data: CreateAuctionParticipantsSchema
    ):
        try:
            NOTIF_TITLE = 'Auction Invitation'
            NOTIF_BODY = (
                "You have been invited to participate in an auction. "
                f"Auction ID: {data.get('auction_id')}"
            )
            user =  await self.user_repo.attachDB(db).get_by_email(data.get('participant_email'))
            if user:
                await self.notify(db, str(user.id), NOTIF_TITLE, NOTIF_BODY)
            _ = await self.participant_repo.attachDB(db).add(data)
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
        db: Session,
        id: str,
        caller: str = 'create',
        existing_amount: float = 0.0
    ):
        try:
            auction = await self.repo.attachDB(db).get_by_id(id)
            bids: list = auction.bids
            winner = None
            if len(bids) > 0:
                winner = max(bids, key=lambda x: x.amount)
            if auction:
                # check if price >= reserve price
                if auction.use_reserve_price and\
                    auction.reserve_price >= winner.amount:
                    await self.repo.attachDB(db).update(
                        auction, {'status': AuctionStatus.CANCLED}
                    )
                    await self.notify(
                        db, auction.users_id, 'Auction Closed',
                        'Your auction has been closed'
                    )
                    for bid in bids:
                        _ = await self.user_repo.attachDB(db).abtw(bid.user_id, bid.amount)
                        await self.notify(
                            db, bid.user_id, 'Auction Lost',
                            'You have lost the auction, Amount has been returned'
                        )
                        return


                await self.repo.attachDB(db).update(
                    auction, {'status': AuctionStatus.COMPLETED}
                )
                await self.notify(
                    db, auction.users_id, 'Auction Closed',
                    'Your auction has been closed'
                )
                await self.payment_repo.attachDB(db).add(
                    CreatePaymentSchema(
                        from_id=winner.user_id, to_id=auction.users_id,
                        auction_id=auction.id, amount=winner.amount,
                        due_data=datetime.now().astimezone()\
                            + timedelta(minutes=10.0)
                    ),
                    caller=caller,
                    existing_amount=existing_amount
                )
                await self.notify(
                    db, winner.user_id, 'Auction Won',
                    'Congratulations, you have won the auction'
                )
                await publish_win_auction(
                    {
                        'auction_id': id,
                        'winner': winner.user_id,
                        'amount': winner.amount
                    }
                )
                # TODO: Develop system to move amount to company's account
                bids = sorted(bids, key=lambda x: x.amount)
                bids = bids[:-1]
                for bid in bids:
                    _ = await self.user_repo.attachDB(db).abtw(bid.user_id, bid.amount)
                    await self.notify(
                        db, bid.user_id, 'Auction Lost',
                        'You have lost the auction, Amount has been returned'
                    )
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def restart(self, db: Session, id: str, data: RestartAuctionSchema):
        try:
            auction = await self.repo.attachDB(db).get_by_id(id)
            payment = await self.payment_repo.attachDB(db).get_by_attr({'auction_id': id})
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
                    await self.payment_repo.attachDB(db).delete(payment)
                # Notify the seller and participants
                await self.notify(
                    db, auction.users_id, 'Auction Restarted',
                    notification_messages.AUCTION_RESTARTED.message,
                    links=[
                        f'{notification_messages.AUCTION_RESTARTED.link[0]}{id}',
                    ],
                    class_name=NotificationClasses.AUCTION.value
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

    async def set_inspecting(self, db: Session, id: str, buyer_id: str):
        try:
            payment = await self.payment_repo.attachDB(db).get_by_attr({'auction_id': id})
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

                await self.payment_repo.attachDB(db).update(
                    payment, {
                        'status': PaymentStatus.INSPECTING,
                        'due_data': datetime.now().astimezone() + timedelta(days=5)
                    }
                )
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def finalize_payment(self, db: Session, auction_id, buyer_id: str):
        try:
            payment = await self.payment_repo.attachDB(db).get_by_attr({'auction_id': auction_id})
            if not payment:
                raise ExcRaiser400(
                    detail='Entity not found'
                )
            payment = GetPaymentSchema.model_validate(payment)
            if payment.from_id != buyer_id:
                raise ExcRaiser400(
                    detail='You are not the buyer of this auction'
                )
            res = await self.payment_repo.attachDB(db).disburse(payment)
            if res:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def refund(self, db:Session, id: str, buyer_id: str):
        try:
            payment = await self.payment_repo.attachDB(db).get_by_attr({'auction_id': id})
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
            res = await self.payment_repo.attachDB(db).update(payment, payment_)

            # Notify the seller and buyer
            await self.notify(
                db, payment.to_id, 'Refund Requested',
                notification_messages.REFUND_REQUEST_SELLER.message,
                links=[
                    f'{notification_messages.REFUND_REQUEST_SELLER.link}{id}',
                ],
                class_name=NotificationClasses.PAYMENT.value
            )

            # Notify the buyer that the refund is being processed
            await self.notify(
                db, payment.from_id, 'Refund Processing',
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

    async def complete_refund(self, db:Session, id: str, seller_id: str):
        try:
            payment = await self.payment_repo.attachDB(db).get_by_attr({'auction_id': id})
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
            res = await self.payment_repo.attachDB(db).refund(payment_)

            # Notify the seller and buyer
            await self.notify(
                db, payment.to_id, 'Refund Requested',
                notification_messages.REFUND_COMPLETED,
                links=[
                    f'{notification_messages.REFUND_COMPLETED.link[0]}{id}',
                ],
                class_name=NotificationClasses.PAYMENT.value
            )

            # Notify the buyer that the refund is being processed
            await self.notify(
                db, payment.from_id, 'Refund Processing',
                notification_messages.REFUND_COMPLETED,
                links=[
                    f'{notification_messages.REFUND_COMPLETED.link[1]}{id}',
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

    async def delete(self, db:Session, id: str):
        try:
            auction = await self.repo.attachDB(db).get_by_id(id)
            bids = auction.bids
            for bid in bids:
                _ = await self.user_repo.attachDB(db).abtw(bid.user_id, bid.amount)
                await self.notify(
                    db, bid.user_id, 'Auction Closed',
                    'The auction has been canceled, The amount placed on the bid has been returned'
                )
            result = await self.repo.attachDB(db).delete(auction)
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
        db:Session,
        user_id: str,
        title: str,
        message: str,
        links: list = None,
        class_name: str = None
    ):
        try:
            notice = CreateNotificationSchema(
                title=title, message=message,
                user_id=user_id, links=links or [],
                class_name=class_name
            )
            await self.notification.create(db, notice)
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def search(
            self,
            db:Session,
            filter: SearchQuery,
        ) -> PagedResponse:
        try:
            filter = filter.model_dump()
            result = await self.repo.attachDB(db).search(filter)
            result.data = [GetAuctionSchema.model_validate(r) for r in result.data]
            return result
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
