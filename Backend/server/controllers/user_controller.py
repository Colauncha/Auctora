from fastapi import APIRouter, Depends, BackgroundTasks, Response
from server.config import get_db, redis_store
from server.enums import ServiceKeys
from server.enums.user_enums import Permissions, UserRoles
from server.middlewares.exception_handler import ExcRaiser
from server.middlewares.auth import permissions
from server.schemas import (
    CreateUserSchema, VerifyOtpSchema,
    APIResponse, UpdateUserSchema,
    GetUserSchema, ResetPasswordSchema,
    LoginSchema, ChangePasswordSchema,
    LoginToken, PagedQuery,
    ErrorResponse, PagedResponse,
    GetUsers, GetNotificationsSchema,
    NotificationQuery,
)
from server.services import UserServices, current_user, UserNotificationServices
from server.utils import Emailer
from sqlalchemy.orm import Session


route = APIRouter(prefix='/users', tags=['users'])
notif_route = APIRouter(prefix='/notifications', tags=['notifications'])
db = Depends(get_db)


###############################################################################
################################# User Endpoints ##############################
###############################################################################

@route.get('/')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def get_users(
    user: current_user,
    filter: PagedQuery = Depends(PagedQuery),
    db: Session = Depends(get_db)
) -> PagedResponse[list[GetUsers]]:
    users = await UserServices(db).list(filter)
    return users


@route.get('/profile')
async def get_user(user: current_user) -> APIResponse[GetUserSchema]:
    return APIResponse(data=user)


@route.get('/retrieve/{id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def retrieve_users(
    user: current_user,
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetUserSchema]:
    """
    Get user
    """
    retrieved_user = await UserServices(db).retrieve(id)
    if retrieved_user.role == UserRoles.ADMIN and user.role != UserRoles.ADMIN:
        raise ExcRaiser(
            status_code=403,
            message='Unauthorized',
            detail='You do not have the permission to access this endpoint'
        )
    return APIResponse(data=retrieved_user)


@route.post(
        '/register',
        responses={
            400: {"model": ErrorResponse}
        }
    )
async def register(
    data: CreateUserSchema,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db)
) -> APIResponse:
    result = await UserServices(db).create_user(data.model_dump(exclude_unset=True))
    emailer = Emailer(
        subject="Email verification",
        to=result.get('email'),
        template_name="otp_template.html",
        otp=result.get('otp')
    )
    emailer = await emailer.enter()
    background_task.add_task(
        emailer.send_message
    )

    return APIResponse(
        data={
            'message':
            'User registered successfully, OTP sent to mail for verification',
        }
    )


@route.post('/register_admin')
@permissions(permission_level=Permissions.ADMIN)
async def register_admin(
    user: current_user,
    data: CreateUserSchema,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db)
) -> APIResponse:
    data = data.model_dump(exclude_unset=True)
    data['role'] = UserRoles.ADMIN
    result = await UserServices(db).create_user(data)
    emailer = Emailer(
        subject="Email verification",
        to=result.get('email'),
        template_name="otp_template.html",
        otp=result.get('otp')
    )
    emailer = await emailer.enter()
    background_task.add_task(
        emailer.send_message
    )

    return APIResponse(
        data={
            'message':
            'Admin registered successfully, OTP sent to mail for verification',
        }
    )


@route.post('/verify_otp')
async def verify_otp(
    data: VerifyOtpSchema,
    db: Session = Depends(get_db)
) -> APIResponse[dict[str, str]]:
    response = await UserServices(db).verify_otp(data)
    return APIResponse(data=response)


@route.post('/reset_otp')
async def reset_otp(
    email: str,
    db: Session = Depends(get_db)
) -> APIResponse[dict[str, str]]:
    response = await UserServices(db).new_otp(email)
    return APIResponse(data=response)
    


@route.post(
        '/login',
        responses={
            401: {"model": ErrorResponse}
        }
    )
async def login(
    credentials: LoginSchema,
    response: Response,
    db: Session = Depends(get_db)
) -> APIResponse[LoginToken]:
    token = await UserServices(db).authenticate(credentials)
    response.set_cookie(
        key='access_token',
        value=token.token,
        httponly=True,
        max_age=180
    )
    return APIResponse(data=token)


@route.put('/update')
@permissions
async def update_user(
    user: current_user,
    data: UpdateUserSchema,
    id: str = None,
    db: Session = Depends(get_db)
) -> APIResponse[bool]:
    id = id if user.role == UserRoles.ADMIN else user.id
    user_ = await UserServices(db).retrieve(id)
    valid_user = GetUserSchema.model_validate(user_)
    result = await UserServices(db).update_user(valid_user, data)
    return APIResponse(data=result)


@route.get('/get_reset_token')
async def get_reset_token(
    email: str,
    db: Session = Depends(get_db)
) -> APIResponse:
    response = await UserServices(db).get_reset_token(email)
    return APIResponse(data=response)


@route.post('/reset_password')
async def reset_password(
    data: ResetPasswordSchema,
    db: Session = Depends(get_db)
) -> APIResponse:
    response = await UserServices(db).reset_password(data)
    return APIResponse(data=response)


@route.post('/update_password')
@permissions(permission_level=Permissions.CLIENT)
async def change_password(
    user: current_user,
    data: ChangePasswordSchema,
    db: Session = Depends(get_db)
) -> APIResponse:
    response = await UserServices(db).change_password(user, data)
    return APIResponse(data=response)


###############################################################################
############################ Notification Endpoints ###########################
###############################################################################

@notif_route.get('/')
@permissions(permission_level=Permissions.CLIENT)
async def list(
    user: current_user,
    filter: PagedQuery = Depends(PagedQuery),
    db: Session = Depends(get_db)
) -> PagedResponse[list[GetNotificationsSchema]]:
    filter = NotificationQuery(**filter.model_dump(), user_id=user.id)
    notifications = await UserNotificationServices(db).list(filter)
    return notifications


@notif_route.get('/{notification_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.NOTIFICATION)
async def retrieve(
    user: current_user,
    notification_id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetNotificationsSchema]:
    notification = await UserNotificationServices(db).retrieve(notification_id)
    return APIResponse(data=notification)


route.include_router(notif_route)
