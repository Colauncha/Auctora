from enum import Enum

class UserRoles(Enum):
    CLIENT = 'client'
    ADMIN = 'admin'


class Permissions(Enum):
    ADMIN = ['admin']
    CLIENT = ['admin', 'client']
    AUTHENTICATED = ['admin', 'client', 'authenticated']
    ALL = ['*']

