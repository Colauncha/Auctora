from functools import wraps
from fastapi import HTTPException
from server.services import current_user
from server.schemas import GetUserSchema
from server.enums.user_enums import UserRoles, Permissions


# Permissions decorator
def permissions(_func=None, *, permission_level: list[str] = Permissions.CLIENT):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user: GetUserSchema = args[0]
            if not GetUserSchema.model_validate(user):
                raise HTTPException(
                    status_code=401,
                    detail='Unauthenticated'
                )
            elif permission_level == Permissions.ADMIN and user.role == UserRoles.ADMIN:
                return f(*args, **kwargs)
            elif permission_level == Permissions.CLIENT and (user.role == UserRoles.ADMIN or user.role == UserRoles.CLIENT):
                return f(*args, **kwargs)
            elif permission_level == Permissions.AUTHENTICATED and user:
                return f(*args, **kwargs)
            else:
                raise HTTPException(
                    status_code=403,
                    detail='Unauthorized'
                )
        return decorated_function
    if _func is None:
        return decorator
    return decorator(_func)