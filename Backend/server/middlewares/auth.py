from functools import wraps
from fastapi import HTTPException
from server.enums import ServiceKeys
from server.enums.user_enums import UserRoles, Permissions
from server.middlewares.exception_handler import ExcRaiser404


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
                    resource_id = kwargs.get(service.path_param)
                    if not resource_id:
                        raise ExcRaiser404("Entity ID not found")
                    ServiceClass = service.service_class
                    ownership_check = await ServiceClass.get_ownership(
                        service.model,
                        resource_id,
                        user.id
                    )
                    if not ownership_check:
                        raise HTTPException(status_code=403, detail='Unauthorized: Ownership required')
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


from fastapi import Depends, HTTPException, Request, status
from server.enums.user_enums import UserRoles, Permissions
from server.services import get_db, AuthServices 
from sqlalchemy.orm import Session

class RequirePermission:
    def __init__(self, permission_level: list[str], service_key: ServiceKeys = ServiceKeys.NONE):
        self.permission_level = permission_level
        self.service_key = service_key

    async def __call__(
        self, 
        request: Request, 
        user = Depends(AuthServices._get_current_user),
        db: Session = Depends(get_db)
    ):
        """
        This method runs automatically when injected into a route.
        """
        # 1. Authentication Check
        if not user:
            raise HTTPException(status_code=401, detail='Unauthenticated')

        # 2. Admin Bypass
        if self.permission_level == Permissions.ADMIN:
            if user.role != UserRoles.ADMIN:
                raise HTTPException(status_code=403, detail='Unauthorized: Admin access required')
            return # Allowed

        # 3. Client/Owner Check
        if self.permission_level == Permissions.CLIENT:
            # Admins can usually access client data too
            if user.role == UserRoles.ADMIN:
                return 

            if user.role != UserRoles.CLIENT:
                 raise HTTPException(status_code=403, detail='Unauthorized')

            # If we need to check ownership of a specific resource
            if self.service_key != ServiceKeys.NONE and self.service_key != ServiceKeys.USER:
                
                # Dynamically extract the ID from the URL (e.g., /items/{item_id})
                resource_id = request.path_params.get(self.service_key.path_param)
                
                if not resource_id:
                    # Route configuration error or logic mismatch
                    raise HTTPException(status_code=400, detail=f"Missing path parameter: {self.service_key.path_param}")

                # Instantiate the service (Assumes Service accepts DB or has a static/class method)
                # Based on your previous code, I assume retrieve is available
                # Note: If your Services are fully DI now, you might need a Factory here.
                # For now, we assume we can manually call the retrieve logic:
                
                try:
                    # We access the class from the Enum, then call retrieve
                    # You might need to adjust this depending on if 'retrieve' is static or instance
                    ServiceClass = self.service_key.service_class
                    # print(f"Checking ownership for service: {ServiceClass.__name__}\n{dir(ServiceClass)}")
                    ownership_check = await ServiceClass.get_ownership(
                        self.service_key.model,
                        resource_id,
                        user.id
                    )
                    if not ownership_check:
                        raise HTTPException(status_code=403, detail='Unauthorized: Ownership required')
                    return # Allowed
                except Exception as e:
                    print(e)
                    raise HTTPException(status_code=500, detail='Internal Server Error during ownership check')

        # 4. Generic Authenticated Check
        if self.permission_level == Permissions.AUTHENTICATED:
            return # Allowed if user exists (checked at top)

        raise HTTPException(status_code=403, detail='Unauthorized')
