import json
import hashlib
import hmac
from typing import Union
from fastapi import APIRouter, Depends, Request, Response
from server.config import get_db, redis_store, app_configs
from server.enums import ServiceKeys
from server.enums.user_enums import (
    Permissions,
    TransactionTypes,
    UserRoles,
    TransactionStatus
)
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser400
from server.middlewares.auth import permissions
from server.schemas import (
    CreateUserSchema, PaystackWebhookSchema, VerifyOtpSchema,
    APIResponse, UpdateUserSchema,
    GetUserSchema, ResetPasswordSchema,
    LoginSchema, ChangePasswordSchema,
    LoginToken, PagedQuery,
    ErrorResponse, PagedResponse,
    GetUsers, GetNotificationsSchema,
    NotificationQuery, UpdateNotificationSchema,
    WalletTransactionSchema, VerifyTransactionData,
    InitializePaymentRes, GetUsersSchemaPublic,
    WalletHistoryQuery, TransferRecipientData,
    AccountDetailsSchema
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
) -> APIResponse[GetUsersSchemaPublic]:
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
    db: Session = Depends(get_db)
) -> APIResponse:
    _ = await UserServices(db).create_user(data.model_dump(exclude_unset=True))
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
    db: Session = Depends(get_db)
) -> APIResponse:
    data = data.model_dump(exclude_unset=True)
    data['role'] = UserRoles.ADMIN
    _ = await UserServices(db).create_user(data)

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
        secure=True,
        samesite="None",
        # partitioned=True
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
    result = await UserNotificationServices(db).update(
        notification_id, data.read
    )
    return APIResponse(data=result)


##############################################################################
############################ Transactions Endpoints ##########################
##############################################################################

@transac_route.get('/history')
@permissions(permission_level=Permissions.CLIENT)
async def list(
    user: current_user,
    filter: WalletHistoryQuery = Depends(),
    db: Session = Depends(get_db)
) -> PagedResponse:
    filter.user_id = user.id
    print(filter)
    result = await UserWalletTransactionServices(db).list(filter)
    return result


@transac_route.get('/init')
@permissions(permission_level=Permissions.CLIENT)
async def get_gateway_url(
    user: current_user,
    amount: int,
    db: Session = Depends(get_db)
) -> InitializePaymentRes:
    url = f"{app_configs.paystack.PAYSTACK_URL}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {app_configs.paystack.SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "amount": amount * 100,
        "email": user.email,
        "metadata": {
            "user_id": str(user.id),
            "amount": amount,
            "email": user.email
        }
    }
    response = requests.post(url, headers=headers, json=data)
    res_data: dict = response.json()
    data = InitializePaymentRes.model_validate(res_data)
    _ = await UserWalletTransactionServices(db).init_transaction(
        data, user, amount
    )
    return data


@transac_route.post('/verify')
@permissions(permission_level=Permissions.CLIENT)
async def verify_funding(
    user: current_user,
    data: VerifyTransactionData,
    db: Session = Depends(get_db)
) -> WalletTransactionSchema:
    extra = {
        'transaction_type': TransactionTypes.FUNDING,
    }
    paystack_url = app_configs.paystack.PAYSTACK_URL
    url = f"{paystack_url}/transaction/verify/{data.reference_id}"
    headers = {
        "Authorization": f"Bearer {app_configs.paystack.SECRET_KEY}"
    }
    response_types = {
        'success': ['success'],
        'failed': ['failed', 'cancelled', 'reversed'],
        'pending': ['pending', 'ongoing', 'processing', 'queued']
    }
    response = requests.get(url, headers=headers)
    res_data: dict = response.json()

    if res_data.get('data').get('status') in response_types['success']:
        extra['status'] = TransactionStatus.COMPLETED
    elif res_data.get('data').get('status') in response_types['pending']:
        extra['status'] = TransactionStatus.PENDING
    elif res_data.get('data').get('status') in response_types['failed']:
        extra['status'] = TransactionStatus.FAILED
    else:
        extra['status'] = TransactionStatus.FAILED

    extra['description'] = (
        f"{res_data.get('message')}: transaction {extra['status'].value}"
    )
    data.amount = float(res_data.get('data').get('amount') / 100)
    data.user_id = str(user.id)
    data.email = user.email
    _ = await UserWalletTransactionServices(db).create(
        data.model_dump(), extra
    )
    return WalletTransactionSchema(**data.model_dump(), **extra)


@transac_route.post('/paystack/webhook')
async def paystack_webhook(
    request: Request,
    db: Session = Depends(get_db)
) -> APIResponse:
    
    signature = request.headers.get("x-paystack-signature")
    ip = request.client.host
    secret = app_configs.paystack.SECRET_KEY.encode()

    if ip not in app_configs.paystack.PAYSTACK_IP_WL:
        raise ExcRaiser400(detail="IP not allowed")
 
    if not signature:
        raise ExcRaiser400(detail="Signature missing")

    data_bytes = await request.body()
    data_json = await request.json()
    hash_obj = hmac.new(secret, data_bytes, hashlib.sha512).hexdigest()

    if not hmac.compare_digest(hash_obj.lower(), signature.lower()):
        raise ExcRaiser400(detail="Invalid signature")

    ...

    data = PaystackWebhookSchema.model_validate(json.loads(data_bytes))
    meta = data_json.get('data').get('metadata')

    extra = {
        'transaction_type': TransactionTypes.FUNDING,
    }

    # Split event string e.g 'charge.success' == ['charge', 'success']
    event, subevent = data.event.split('.')
    if event == 'charge':
        tranx = {
            "user_id": meta.get('user_id'),
            "email": meta.get('email'),
            "amount": meta.get('amount'),
            "reference_id": data.data.reference
        }
        if subevent == 'success':
            extra["status"] = TransactionStatus.COMPLETED
        else:
            extra["status"] = TransactionStatus.FAILED
        extra['description'] = (
            f"{data.data.message}: transaction {extra['status'].value}"
        )
        _ = await UserWalletTransactionServices(db).create(tranx, extra)

    elif event == 'transfer':
        if subevent == 'success':
            ...
        else:
            ...
    return APIResponse()


@transac_route.get('/resolve')
async def resolve_acct_number(
    account_number: str,
    bank_code: str
) -> APIResponse:
    url = f"{app_configs.paystack.PAYSTACK_URL}/bank/resolve"
    headers = {
        "Authorization": f"Bearer {app_configs.paystack.SECRET_KEY}"
    }
    params = {
        "account_number": account_number,
        "bank_code": bank_code
    }
    response = requests.get(url, headers=headers, params=params)
    res_data: dict = response.json()
    return res_data


@transac_route.post('/transfer_recipient')
@permissions(permission_level=Permissions.CLIENT)
async def transfer_recipient(
    user: current_user,
    data: TransferRecipientData,
    db: Session = Depends(get_db)
) -> Union[APIResponse, dict]:
    url_resolve = f"{app_configs.paystack.PAYSTACK_URL}/bank/resolve"
    url_tr = f"{app_configs.paystack.PAYSTACK_URL}/transferrecipient"
    headers = {
        "Authorization": f"Bearer {app_configs.paystack.SECRET_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "account_number": data.account_number,
        "bank_code": data.bank_code
    }
    resolve_res = requests.get(url_resolve, headers=headers, params=params)
    resolve_res_data: dict = resolve_res.json()

    # TODO: save recipient code to user model

    if not resolve_res_data.get('data'):
        resolve_message = resolve_res_data.get('message')
        return APIResponse(message=resolve_message, data=None)
    data.name = resolve_res_data.get('data').get('account_name')
    response = requests.post(url_tr, headers=headers, json=data.model_dump())
    response = response.json().get('data')

    if response.get('active') is False:
        return APIResponse(message="Account not active")

    account_data = AccountDetailsSchema(
        acct_no=data.account_number,
        acct_name=data.name,
        bank_code=data.bank_code,
        bank_name=response.get('details').get('bank_name'),
        recipient_code=response.get('recipient_code'),
        id=str(user.id)
    )

    acct_data = await UserServices(db).add_recipient_code(account_data, user)
    return APIResponse(data=acct_data)


@transac_route.post('/withdraw')
@permissions(permission_level=Permissions.CLIENT)
async def withdraw(
    user: current_user,
    amount: int,
    db: Session = Depends(get_db)
) -> APIResponse:
    pass


route.include_router(notif_route)
route.include_router(transac_route)
