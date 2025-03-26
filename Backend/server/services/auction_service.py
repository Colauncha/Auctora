from sqlalchemy.orm import Session
from fastapi import WebSocket
from server.config import redis_store
from server.repositories import DBAdaptor
from server.models.items import Items
from server.enums.auction_enums import AuctionStatus
from server.events.publisher import publish_win_auction
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404, ExcRaiser500, ExcRaiser400
)
from server.services.user_service import (
    UserNotificationServices, UserServices
)
from server.schemas import (
    GetAuctionSchema, AuctionParticipantsSchema,
    CreateNotificationSchema, CreateAuctionParticipantsSchema,
    PagedQuery, PagedResponse, GetUserSchema, CreatePaymentSchema
)


class AuctionServices:
    def __init__(self, db: Session):
        self.repo = DBAdaptor(db).auction_repo
        self.participant_repo = DBAdaptor(db).auction_p_repo
        self.user_repo = UserServices(db).repo
        self.notification = UserNotificationServices(db).create
        self.payment_repo = DBAdaptor(db).payment_repo

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
                        {'auction_id': result.id, 'participant_email': p}
                    )
            await self.notify(
                user_id, NOTIF_TITLE,
                NOTIF_BODY_PRIV if result.private else NOTIF_BODY
            )
            return GetAuctionSchema.model_validate(result)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e # Edit line

    async def retrieve(self, id: str):
        try:
            result = await self.repo.get_by_id(id)
            if not result:
                raise ExcRaiser404("Auction not found")
            return GetAuctionSchema.model_validate(result)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    async def list(
            self,
            filter: PagedQuery,
            extra: dict = None
        ) -> PagedResponse[list[GetAuctionSchema]]:
        try:
            filter = filter.model_dump(exclude_unset=True)
            filter['private'] = False
            if extra:
                filter.update(extra)
            result = await self.repo.get_all(filter)
            result = [GetAuctionSchema.model_validate(r) for r in result.data]
            return result
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e
        
    async def update(self, id: str, data: dict):
        try:
            print(data)
            entity = await self.repo.get_by_id(id)
            updated = await self.repo.update(entity, data)
            return GetAuctionSchema.model_validate(updated)
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    # Auction participants
    async def create_participants(
            self,
            data: CreateAuctionParticipantsSchema
    ):
        try:
            NOTIF_TITLE = 'Auction Invitation'
            NOTIF_BODY = (
                "You have been invited to participate in an auction. "
                f"Auction ID: {data.get('auction_id')}"
            )
            user =  await self.user_repo.get_by_email(data.get('participant_email'))
            if user:
                await self.notify(str(user.id), NOTIF_TITLE, NOTIF_BODY)
            _ = await self.participant_repo.add(data)
        except Exception as e:
            raise e
        
    async def ws_bids(self, auction_id: str, ws: WebSocket):
        try:
            async_redis = await redis_store.get_async_redis()
            bid_list = async_redis.get(f'auction:{auction_id}')
            await ws.send(bid_list)
        except Exception as e:
            raise e

    async def close(self, id: str):
        try:
            auction = await self.repo.get_by_id(id)
            if auction:
                await self.repo.update(
                    auction, {'status': AuctionStatus.COMPLETED}
                )
                self.notify(
                    auction.users_id, 'Auction Closed',
                    'Your auction has been closed'
                )
                bids: list = auction.bids
                winner = max(bids, key=lambda x: x.amount)
                await self.payment_repo.add(
                    CreatePaymentSchema(
                        from_id=winner.id, to_id=auction.users_id,
                        auction_id=auction.id, amount=winner.amount
                    )
                )
                await self.notify(
                    winner.user_id, 'Auction Won',
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
                print(bid.amount for bid in bids)
                bids = bids[:-1]
                for bid in bids:
                    _ = await self.user_repo.abtw(bid.user_id, bid.amount)
                    await self.notify(
                        bid.user_id, 'Auction Lost',
                        'You have lost the auction, Amount has been returned'
                    )
        except Exception as e:
            raise e

    async def delete(self, id: str):
        ...

    # Notifications
    async def notify(self, user_id: str, title: str, message: str):
        try:
            notice = CreateNotificationSchema(
                title=title, message=message,
                user_id=user_id
            )
            await self.notification(notice)
        except Exception as e:
            raise e
