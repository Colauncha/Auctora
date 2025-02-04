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
    FUNDING = 'FUNDING'
    WITHDRAWAL = 'WITHDRAWAL'
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'


class TransactionStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'