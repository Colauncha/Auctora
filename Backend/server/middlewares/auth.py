from functools import wraps
from typing import Union
from fastapi import HTTPException
from server.services import current_user
from server.schemas import GetUserSchema
from server.enums import ServiceKeys
from server.enums.user_enums import UserRoles, Permissions
from server.middlewares.exception_handler import ExcRaiser500, ExcRaiser404
from enum import Enum


# Permissions decorator
def permissions(
        _func=None, *, permission_level: list[str] = Permissions.CLIENT,
        service: ServiceKeys = None
    ):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            user = kwargs.get('user')
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail='Unauthenticated'
                )
            elif permission_level == Permissions.ADMIN and user.role == UserRoles.ADMIN:
                return await f(*args, **kwargs)
            elif permission_level == Permissions.CLIENT and (user.role == UserRoles.ADMIN or user.role == UserRoles.CLIENT):
                if service and service != ServiceKeys.USER:
                    entity_id = kwargs.get(service.id)
                    if not entity_id:
                        raise ExcRaiser404("Entity ID not found")
                    entity = await service.service(kwargs.get('db')).retrieve(entity_id)
                    if (entity.users_id != user.id) or (entity.user_id != user.id) or (entity.id != user.id):
                        raise HTTPException(
                            status_code=403,
                            detail='Unauthorized'
                        )
                return await f(*args, **kwargs)
            elif permission_level == Permissions.AUTHENTICATED and user:
                return await f(*args, **kwargs)
            else:
                raise HTTPException(
                    status_code=403,
                    detail='Unauthorized'
                )
        return decorated_function
    if _func is None:
        return decorator
    return decorator(_func)