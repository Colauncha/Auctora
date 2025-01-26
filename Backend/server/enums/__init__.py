from enum import Enum
from server.services.item_service import ItemServices
from server.services.user_service import UserServices, UserNotificationServices
from server.services.category_service import CategoryServices
from server.services.auction_service import AuctionServices


class ServiceKeys(Enum):
    NONE = (None, None)
    USER = ('id', UserServices)
    ITEM = ('item_id', ItemServices)
    CATEGORY = ('category_id', CategoryServices)
    AUCTION = ('auction_id', AuctionServices)
    NOTIFICATION = ('notification_id', UserNotificationServices)


    def __init__(self, id, service):
        self.id = id
        self.service = service