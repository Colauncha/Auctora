from enum import Enum

class UserRoles(Enum):
    CLIENT = 'client'
    ADMIN = 'admin'


class Permissions(Enum):
    ADMIN = ['admin']
    CLIENT = ['admin', 'client']
    AUTHENTICATED = ['admin', 'client', 'authenticated']
    ALL = ['*']


class TransactionTypes(Enum):
    FUNDING = 'funding'
    WITHDRAWAL = 'withdrawal'
    CREDIT = 'credit'
    DEBIT = 'debit'


class TransactionStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'