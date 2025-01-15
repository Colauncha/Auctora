from enums import Enum


class AuctionStatus(Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCLED = 'cancled'
    PENDING = 'pending'
