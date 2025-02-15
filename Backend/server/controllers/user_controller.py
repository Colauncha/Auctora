from fastapi import APIRouter, Depends, BackgroundTasks, Response
from server.config import get_db, redis_store, app_configs
from server.enums import ServiceKeys
from server.enums.user_enums import Permissions, TransactionTypes, UserRoles, TransactionStatus
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
    NotificationQuery, UpdateNotificationSchema,
    WalletTransactionSchema, VerifyTransactionData,
    InitializePaymentRes
)
from server.services import (
    UserServices,
    current_user,
    UserNotificationServices,
    UserWalletTransactionServices
)
from server.utils import Emailer
from sqlalchemy.orm import Session
import requests


route = APIRouter(prefix='/users', tags=['users'])
notif_route = APIRouter(prefix='/notifications', tags=['notifications'])
transac_route = APIRouter(prefix='/transactions')
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
        max_age=1800,
        samesite="lax"
    )
    return APIResponse(data=token)


@route.post('/logout')
async def logout(response: Response) -> APIResponse[str]:
    response.delete_cookie(key='access_token')
    return APIResponse(data='Logout successful')


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
    filter: NotificationQuery = Depends(NotificationQuery),
    db: Session = Depends(get_db)
) -> PagedResponse[list[GetNotificationsSchema]]:
    filter.user_id = user.id
    filter = NotificationQuery(**filter.model_dump())
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


@notif_route.put('/{notification_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.NOTIFICATION)
async def update(
    user: current_user,
    notification_id: str,
    data: UpdateNotificationSchema,
    db: Session = Depends(get_db)
) -> APIResponse:
    result = await UserNotificationServices(db).update(notification_id, data.read)
    return APIResponse(data=result)


###############################################################################
############################ Transactions Endpoints ###########################
###############################################################################

@transac_route.get('/init')
@permissions(permission_level=Permissions.CLIENT)
async def get_gateway_url(
    user: current_user,
    amount: str
) -> InitializePaymentRes:
    url = f"{app_configs.paystack.PAYSTACK_URL}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {app_configs.paystack.SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "amount": amount * 100,
        "email": user.email,
    }
    response = requests.post(url, headers=headers, json=data)
    res_data: dict = response.json()
    return InitializePaymentRes.model_validate(res_data)


@transac_route.post('/verify')
@permissions(permission_level=Permissions.CLIENT)
async def verify_funding(
    user: current_user,
    data: VerifyTransactionData,
    db: Session = Depends(get_db)
) -> WalletTransactionSchema:
    extra = {
        'transaction_type': TransactionTypes.CREDIT,
    }
    url = f"{app_configs.paystack.PAYSTACK_URL}/transaction/verify/{data.reference_id}"
    headers = {
        "Authorization": f"Bearer {app_configs.paystack.SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)
    res_data: dict = response.json()
    if res_data.get('data').get('status') == 'success':
        extra['status'] = TransactionStatus.COMPLETED
        extra['description'] = res_data.get('message')
        data.amount = float(res_data.get('data').get('amount') / 100)
    else:
        extra['status'] = TransactionStatus.FAILED
        extra['description'] = res_data.get('message')
    data.user_id = str(user.id)
    data.email = user.email
    _ = await UserWalletTransactionServices(db).create(data.model_dump(), extra)
    return WalletTransactionSchema(**data.model_dump(), **extra)


route.include_router(notif_route)
route.include_router(transac_route)
