from sqlalchemy.orm import Session
from server.repositories import DBAdaptor
from server.models.items import Items
from server.enums.auction_enums import AuctionStatus
# from server.events.publisher import p
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404, ExcRaiser500, ExcRaiser400
)
from server.services.user_service import (
    UserNotificationServices, UserServices
)
from server.schemas import (
    GetAuctionSchema, AuctionParticipantsSchema,
    CreateNotificationSchema, CreateAuctionParticipantsSchema,
    PagedQuery, PagedResponse,
)


class AuctionServices:
    def __init__(self, db: Session):
        self.repo = DBAdaptor(db).auction_repo
        self.participant_repo = DBAdaptor(db).auction_p_repo
        self.user_repo = UserServices(db).repo
        self.notification = UserNotificationServices(db).create

    # Auction services
    async def create(self, data: dict):
        try:
            NOTIF_TITLE = "New Auction"
            NOTIF_BODY = "Your new auction has been created"
            NOTIF_BODY_PRIV = "Your new private auction has been created \
                and the participants have been notified"
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
            print((type(e)))
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    async def list(self, filter: PagedQuery) -> PagedResponse[list[GetAuctionSchema]]:
        try:
            result = await self.repo.get_all(filter.model_dump(exclude_unset=True))
            if result:
                valid_auctions = [
                    GetAuctionSchema.model_validate(auction).model_dump()
                    for auction in result.data
                    if auction.private is False
                ]
                result.data = valid_auctions
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
            NOTIF_BODY = f"You have been invited to participate in an auction.\
                Auction ID: {data.get('auction_id')}"
            user =  await self.user_repo.get_by_email(data.get('participant_email'))
            if user:
                await self.notify(str(user.id), NOTIF_TITLE, NOTIF_BODY)
            _ = await self.participant_repo.add(data)
        except Exception as e:
            raise e
        
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
