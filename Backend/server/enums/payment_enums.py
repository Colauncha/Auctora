from enum import Enum

class PaymentStatus(Enum):
    INSPECTING = 'inspecting'
    PENDING = 'pending'
    COMPLETED = 'completed'
    REFUNDED = 'refunded'
    REFUNDING = 'refunding'
