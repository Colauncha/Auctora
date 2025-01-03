from functools import wraps
from fastapi import HTTPException
from server.services import current_user
from server.schemas import GetUserSchema
from server.enums.user_enums import UserRoles, Permissions
from server.middlewares.exception_handler import ExcRaiser500


# Permissions decorator
def permissions(_func=None, *, permission_level: list[str] = Permissions.CLIENT):
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