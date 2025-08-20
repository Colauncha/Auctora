from enum import Enum
from server.services import Services


class ServiceKeys(Enum):
    NONE = (None, None)
    USER = ('id', Services.userServices)
    ITEM = ('item_id', Services.itemServices)
    CATEGORY = ('category_id', Services.categoryServices)
    AUCTION = ('auction_id', Services.auctionServices)
    NOTIFICATION = ('notification_id', Services.notificationServices)
    BID = ('bid_id', Services.bidServices)
    WALLET = ('transaction_id', Services.walletServices)


    def __init__(self, id, service):
        self.id = id
        self.service = service
