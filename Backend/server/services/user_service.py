from uuid import uuid4
from jose import jwt
from datetime import datetime, timezone, timedelta
import inspect

from sqlalchemy.orm import Session
from server.models.users import Users
from server.enums.user_enums import TransactionStatus, TransactionTypes, UserRoles
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from server.config import app_configs, redis_store
from jose.exceptions import JWTError
from server.utils import (
    is_valid_email,
    otp_generator,
    generate_referral_code,
    decode_referral_code
)
from server.schemas import (
    VerifyOtpSchema, LoginSchema,
    GetUserSchema, UpdateUserSchema,
    LoginToken, ResetPasswordSchema,
    ChangePasswordSchema, PagedResponse,
    PagedQuery, GetUsers, GetNotificationsSchema,
    NotificationQuery, CreateNotificationSchema,
    WalletTransactionSchema, WalletHistoryQuery,
    InitializePaymentRes, AccountDetailsSchema,
    UpdateUserAddressSchema, ReferralSlots
)
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404, ExcRaiser500, ExcRaiser400
)
from server.events import (
    publish_reset_token,
    publish_otp,
    publish_fund_account
)
from fastapi import HTTPException


oauth_bearer = OAuth2PasswordBearer(tokenUrl=f"api/users/login")


###############################################################################
############################ Notification Services ############################
###############################################################################

class UserNotificationServices:
    def __init__(self, notif_repo):
        self.repo = notif_repo
        self.debug = app_configs.DEBUG

    async def list(self, db: Session, notice: NotificationQuery):
        try:
            result = await self.repo.attachDB(db).get_all(notice.model_dump(exclude_unset=True))
            if not result:
                raise ExcRaiser404(message='No Notification found')
            valid_notices = [
                GetNotificationsSchema.model_validate(notice).model_dump()
                for notice in result.data
            ]
            result.data = valid_notices
            return result
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def retrieve(self, db: Session, id: str):
        try:
            notice = await self.repo.attachDB(db).get_by_id(id)
            if notice:
                valid_notice = GetNotificationsSchema.model_validate(notice)
                return valid_notice
            raise ExcRaiser404(message='Notification not found')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def create(self, db: Session, data: CreateNotificationSchema):
        try:
            result = await self.repo.attachDB(db).add(data.model_dump())
            if result:
                return GetNotificationsSchema.model_validate(result)
            raise ExcRaiser400(message='Unable to create Notification')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def update(self, db: Session, id: str, read: bool):
        try:
            notice = await self.repo.attachDB(db).get_by_id(id)
            if notice:
                result = await self.repo.attachDB(db).save(notice, {'read': read})
                if result:
                    return True
            raise ExcRaiser404(message='Notification not found')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))


###############################################################################
############################ Notification Services ############################
###############################################################################

class UserWalletTransactionServices:
    def __init__(self, notif_repo, user_repo, notif_service):
        self.repo = notif_repo
        self.user_repo = user_repo
        self.notification = notif_service
        self.debug = app_configs.DEBUG

    async def init_transaction(
        self,
        db: Session,
        data: InitializePaymentRes ,
        user: GetUserSchema,
        amount: float,
        t_type: TransactionTypes = TransactionTypes.FUNDING
    ):
        try:
            wallet_data = WalletTransactionSchema.model_validate({
                "user_id": user.id,
                "status": TransactionStatus.PENDING,
                "transaction_type": t_type,
                "description": f"{t_type} of {amount} pending",
                "amount": amount,
                "reference_id": data.data.reference
            })
            _ = await self.repo.attachDB(db).add(wallet_data.model_dump())
            return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def create(self, db: Session, transaction, extra):
        try:
            transaction = WalletTransactionSchema(**transaction, **extra)
            user = await self.user_repo.attachDB(db).get_by_id(transaction.user_id)
            notify = False

            print(transaction, user)
            NOTIF_TITLE = f"Funding Account {transaction.status.value}"
            NOTIF_MESSAGE = (
            f"Your attempt to credit your wallet with N{transaction.amount} "
            f"has {transaction.status.value}"
            )

            exist = await self.repo.attachDB(db).get_by_attr(
                {'reference_id': transaction.reference_id}
            )

            if transaction.status == TransactionStatus.COMPLETED:
                if exist and exist.status == transaction.status:
                    return
                elif exist and exist.status != transaction.status:
                    _ = await self.user_repo.attachDB(db).fund_wallet(
                        transaction, update=True, exist=exist
                    )
                    notify = True
                elif not exist:
                    _ = await self.user_repo.attachDB(db).fund_wallet(transaction)
                    notify = True

            else:
                if exist and exist.status == transaction.status:
                    return
                elif exist and exist.status != transaction.status:
                    _ = await self.repo.attachDB(db).save(exist, transaction.model_dump())
                else:
                    _ = await self.repo.attachDB(db).add(transaction.model_dump())
                    notify = True
            

            if notify:
                pub_data = transaction.model_dump()
                pub_data['email'] = user.email
                _ = await self.notification.create(
                    db,
                    CreateNotificationSchema(
                        title=NOTIF_TITLE,
                        message=NOTIF_MESSAGE,
                        user_id=user.id
                    )
                )
                # await publish_fund_account(pub_data)
            return
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def list(self, db: Session, filter: WalletHistoryQuery):
        try:
            filter = filter.model_dump(exclude_none=True)
            history = await self.repo.attachDB(db).get_all(filter=filter)
            if not history:
                raise ExcRaiser404(message='No Transaction found')
            valid_history = [
                WalletTransactionSchema
                .model_validate(transaction)
                .model_dump()
                for transaction in history.data
            ]
            history.data = valid_history
            return history
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def withdraw(self, db: Session, transaction, extra) -> bool:
        try:
            transaction = WalletTransactionSchema(**transaction, **extra)
            user = await self.user_repo.attachDB(db).get_by_id(transaction.user_id)
            notify = False

            print(transaction, user)
            NOTIF_TITLE = f"Funding Account {transaction.status.value}"
            NOTIF_MESSAGE = (
            f"Your attempt to withdraw N{transaction.amount} from your wallet"
            f"was {transaction.status.value}"
            )

            exist = await self.repo.attachDB(db).get_by_attr(
                {'reference_id': transaction.reference_id}
            )

            if transaction.status == TransactionStatus.COMPLETED:
                if exist and exist.status == transaction.status:
                    return
                elif exist and exist.status != transaction.status:
                    _ = await self.user_repo.attachDB(db).withdraw(
                        transaction, update=True, exist=exist
                    )
                    notify = True
                elif not exist:
                    _ = await self.user_repo.attachDB(db).withdraw(transaction)
                    notify = True

            else:
                if exist and exist.status == transaction.status:
                    return
                elif exist and exist.status != transaction.status:
                    _ = await self.repo.attachDB(db).save(exist, transaction.model_dump())
                else:
                    _ = await self.repo.attachDB(db).add(transaction.model_dump())
                    notify = True
            

            if notify:
                pub_data = transaction.model_dump()
                pub_data['email'] = user.email
                _ = await self.notification.create(
                    db,
                    CreateNotificationSchema(
                        title=NOTIF_TITLE,
                        message=NOTIF_MESSAGE,
                        user_id=user.id
                    )
                )
                # await publish_fund_account(pub_data)
            return
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def retrieve(self, db: Session, reference: str):
        try:
            transaction = await self.repo.attachDB(db).get_by_attr(
                {'reference_id': reference}
            )
            if transaction:
                valid_transaction = WalletTransactionSchema.model_validate(transaction)
                return valid_transaction
            raise ExcRaiser404(message='Transaction not found')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

##############################################################################
################################ User Services ###############################
##############################################################################

class UserServices:
    def __init__(self, user_repo, notif_service):
        self.repo = user_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.notification = notif_service
        self.debug = app_configs.DEBUG

    def __check_password(self, password, hashed_password) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    async def __generate_token(self, user: Users) -> LoginToken:
        expires_at = datetime.now(tz=timezone.utc) + timedelta(
            minutes=app_configs.security.ACCESS_TOKEN_EXPIRES
        )
        claims = {
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "exp": expires_at,
        }

        token_type = "bearer"
        try:
            token = jwt.encode(
                claims,
                app_configs.security.JWT_SECRET_KEY,
                app_configs.security.ALGORITHM,
            )
        except JWTError as err:
            raise ValueError(err, "Unable to generate token")
        return LoginToken(**{"token": token, "token_type": token_type})

    async def authenticate(self, db: Session, identity: LoginSchema) -> LoginToken:
        try:
            user = None
            if is_valid_email(identity.identifier):
                user = await self.repo.attachDB(db).get_by_email(identity.identifier)
            else:
                user = await self.repo.attachDB(db).get_by_username(identity.identifier)
            if user and self.__check_password(
                    identity.password, user.hash_password
                ):
                token = await self.__generate_token(user)
                return token
            else:
                raise ExcRaiser(
                    status_code=401,
                    message='Unauthorized',
                    detail='Invalid credentials, try again'
                )
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def update_referral_users(
        self,
        db: Session,
        referrer: GetUserSchema,
        referree: GetUserSchema,
    ):
        try:
            refered_slots = referrer.referred_users.copy()
            if not referrer.referral_code:
                raise ExcRaiser400(
                    message='Referrer not eligible for referrals, Proceed to Login'
                )

            # new data
            refered_user = ReferralSlots(
                user_id=str(referree.id), email=referree.email
            )
            refered_slots[f'slot_{referree.email}'] = refered_user.model_dump()
            _ = await self.repo.attachDB(db).update_jsonb(referrer.id, refered_slots)

            return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def create_user(self, db: Session, data: dict) -> dict[str, str]:
        try:
            NOTIF_TITLE = "Welcome to Biddius"
            NOTIF_MESSAGE = (
                "Thank you for signing up with Biddius. "
                "We are glad to have you on board"
            )
            # Check if email already exist
            referral_code = data.pop('referral_code') if data.get('referral_code') else None
            ex_uname = await self.repo.attachDB(db).get_by_username(data.get('username'))\
            if data.get('username') else None
            ex_email = await self.repo.attachDB(db).get_by_email(data.get('email'))
            if ex_email or ex_uname:
                raise ExcRaiser400(detail='Username or email already exist')

            # Create new user
            else:
                new_user = await self.repo.attachDB(db).add(data)
                if not new_user:
                    raise ExcRaiser(
                        message="Unable to create User",
                        status_code=400,
                        detail="Unable to create User"
                    )

                new_user = GetUserSchema.model_validate(new_user)
                # Create a notification for the new user
                _ = await self.notification.create(
                    db,
                    CreateNotificationSchema(
                        title=NOTIF_TITLE,
                        message=NOTIF_MESSAGE,
                        user_id=new_user.id
                    )
                )

                # referral
                if referral_code:
                    ref_username = decode_referral_code(referral_code)
                    ref_user = await self.repo.attachDB(db).get_by_username(ref_username)
                    _ = await self.repo.attachDB(db).update(
                        new_user, {'referred_by': str(ref_user.id)}
                    )
                    await self.update_referral_users(db, ref_user, new_user)

                # OTP
                otp = otp_generator()
                async_redis = await redis_store.get_async_redis()
                _ = await async_redis.set(f'otp:{new_user.email}', otp, ex=1800)
                # url = f"http://link.to.frontend/verify_otp?id={id}&otp={otp}"
                data = {
                    'email': new_user.email,
                    'otp': otp,
                }
                await publish_otp(data)
                return data

        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def create_admin(self, db: Session, data: dict):
        try:
            ex_uname = await self.repo.attachDB(db).get_by_username(data.get('username'))
            ex_email = await self.repo.attachDB(db).get_by_email(data.get('email'))
            if ex_email or ex_uname:
                raise ExcRaiser400(message='User already exist')
            data['role'] = UserRoles.ADMIN
            new_user = await self.repo.attachDB(db).add(data)
            new_user = GetUserSchema.model_validate(new_user)
            # Create a notification for the new user
            _ = await self.notification.create(
                db,
                CreateNotificationSchema(
                    title="ADMIN Registration",
                    message="You have been registered as an Admin",
                    user_id=new_user.id
                )
            )
            otp = otp_generator()
            async_redis = await redis_store.get_async_redis()
            _ = await async_redis.set(f'otp:{new_user.email}', otp, ex=1800)
            data = {
                'email': new_user.email,
                'otp': otp,
            }
            await publish_otp(data)
            return data
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def add_recipient_code(
        self,
        db: Session,
        data: AccountDetailsSchema,
        user: GetUserSchema
    ) -> AccountDetailsSchema:
        try:
            data = data.model_dump(exclude={'id'})
            res = await self.repo.attachDB(db).update(user, data)
            return AccountDetailsSchema.model_validate(*res)
        except Exception as e:
            raise e

    async def retrieve(self, db: Session, id) -> GetUserSchema:
        try:
            user = await self.repo.attachDB(db).get_by_attr({'id': id})
            if user:
                valid_user = GetUserSchema.model_validate(user)
                return valid_user
            raise ExcRaiser404(message='User not found')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    # Not optimal (The auction list should be trauncated)
    async def list(self, db: Session, filter: PagedQuery) ->PagedResponse[list[GetUsers]]:
        try:
            result = await self.repo.attachDB(db).get_all(filter.model_dump(exclude_unset=True))
            if result:
                valid_users = [
                    GetUsers.model_validate(user).model_dump(include={'__all__'})
                    for user in result.data
                ]
                return PagedResponse(
                    data=valid_users,
                    page_number=result.page_number,
                    pages=result.pages,
                    count=result.count,
                    total=result.total,
                    per_page=result.per_page
                )
            raise ExcRaiser404(message='No User found')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def new_otp(self, db: Session, email: str):
        try:
            async_redis = await redis_store.get_async_redis()
            stored_otp = await async_redis.get(f'otp:{email}')
            if stored_otp:
                _ = await async_redis.delete(f'otp:{email}')
            user = await self.repo.attachDB(db).get_by_email(email)
            if user.email_verified:
                return {'detail': 'User email already verified'}
            otp = otp_generator()
            _ = await async_redis.set(f'otp:{email}', otp, ex=1800)
            data = {'email': email, 'otp': otp}
            await publish_otp(data)
            return {'detail': 'OTP resent to Email'}
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def verify_otp(self, db: Session, data: VerifyOtpSchema):
        try:
            NOTIF_TITLE = "Email Verification"
            NOTIF_MESSAGE = "Your email has been verified successfully"
            async_redis = await redis_store.get_async_redis()
            stored_otp = await async_redis.get(f'otp:{data.email}')
            user = await self.repo.attachDB(db).get_by_email(data.email)
            if stored_otp == data.otp:
                _ = await self.repo.attachDB(db).save(user, {'email_verified': True})
                _ = await async_redis.delete(f'otp:{data.email}')
                _ = await self.notification.create(
                    db,
                    CreateNotificationSchema(
                        title=NOTIF_TITLE,
                        message=NOTIF_MESSAGE,
                        user_id=user.id
                    )
                )
                return {'message': 'email verified'}
            raise ExcRaiser400(message='Invalid OTP, mail not verified')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def update_user(self, db: Session, user: GetUserSchema, data: UpdateUserSchema):
        try:
            if not user:
                raise HTTPException(
                    status_code=400, detail="Not authenticated"
                )
            _data = data.model_dump(exclude_unset=True, exclude_none=True)
            ex_uname = await self.repo.attachDB(db).get_by_username(_data.get('username'))
            if ex_uname and ex_uname.id != user.id:
                raise ExcRaiser400(detail='Username already exist')
            result = await self.repo.attachDB(db).update(user, _data)
            if result:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def update_address(
        self,
        db: Session,
        user: GetUserSchema,
        data: UpdateUserAddressSchema
    ):
        try:
            if not user:
                raise HTTPException(
                    status_code=400, detail="Not authenticated"
                )
            _data = data.model_dump(exclude_unset=True, exclude_none=True)
            result = await self.repo.attachDB(db).update(user, _data)
            if result:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def get_reset_token(self, db: Session, email: str):
        try:
            user = await self.repo.attachDB(db).get_by_email(email)
            if not user:
                raise ExcRaiser404("User not found")
            token = uuid4().hex
            async_redis = await redis_store.get_async_redis()
            _ = await async_redis.set(f'reset_password:{email}', token, ex=1800)
            data = {'email': email, 'token': token}
            await publish_reset_token(data)
            return {'detail': 'Reset token sent to email'}
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def reset_password(self, db: Session, data: ResetPasswordSchema):
        try:
            async_redis = await redis_store.get_async_redis()
            stored_token = await async_redis.get(f'reset_password:{data.email}')
            if stored_token == data.token: 
                if data.password == data.confirm_password:
                    user = await self.repo.attachDB(db).get_by_email(data.email)
                    _ = await self.repo.attachDB(db).save(
                        user, {'hash_password': self.pwd_context.hash(data.password)}
                    )
                    _ = await async_redis.delete(f'reset_password:{data.email}')
                    return {'detail': 'Password reset successful'}
                raise ExcRaiser400(detail='Passwords do not match')
            raise ExcRaiser400(detail= 'Invalid token or email')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
        
    async def change_password(self, db: Session, user: GetUserSchema, data: ChangePasswordSchema):
        try:
            user = await self.repo.attachDB(db).get_by_email(user.email)
            if not self.__check_password(data.old_password, user.hash_password):
                raise ExcRaiser400(detail='Invalid old password')
            if data.new_password == data.confirm_password:
                _ = await self.repo.attachDB(db).save(
                    user, {'hash_password': self.pwd_context.hash(data.new_password)}
                )
                return {'detail': 'Password change successful'}
            raise ExcRaiser400(detail='Passwords do not match')
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def get_referral_code(self, db: Session, user: GetUserSchema):
        try:
            username = user.username
            if not username:
                raise ExcRaiser400(
                    message='Username not found',
                    detail="Update profile to include username then proceed"
                )
            if user.referral_code:
                return {
                    'referral_code': user.referral_code,
                    'referral_url': f"{app_configs.FRONTEND_URL}/sign-up?referral_code={user.referral_code}",
                    'referred_users': user.referred_users
                }
            ref_code = generate_referral_code(username)
            _ = await self.repo.attachDB(db).update(
                user, {'referral_code': ref_code}
            )
            return {
                'referral_code': ref_code,
                'referral_url': f"{app_configs.FRONTEND_URL}/sign-up?referral_code={ref_code}"
            }
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def delete_user(self, db: Session, user: GetUserSchema):
        try:
            user_ = await self.repo.attachDB(db).get_by_id(user.id)
            result = await self.repo.attachDB(db).delete(user_)
            if result:
                return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def google_auth(self, db: Session, data: dict):
        try:
            user = await self.repo.get_by_email(data.get('email'))
            if not user:
                NOTIF_TITLE = "Welcome to Biddius"
                NOTIF_MESSAGE = (
                    "Thank you for signing up with Biddius. "
                    "We are glad to have you on board"
                )
                new_user_dict = {
                    'email': data.get('email'),
                    'first_name': data.get('given_name'),
                    'last_name': data.get('family_name'),
                    'username': data.get('email'),
                    'email_verified': True,
                    'image_link': data.get('picture'),
                    'password': data.get('sub'),
                    'role': UserRoles.CLIENT,
                    'google_id': data.get('sub'),
                }
                new_user = await self.repo.attachDB(db).add(new_user_dict)
                if not new_user:
                    raise ExcRaiser400(detail='Unable to create user')

                token = await self.__generate_token(new_user)
                url = f"{app_configs.FRONTEND_URL}/oauth-success"
                new_user = GetUserSchema.model_validate(new_user)
                # Create a notification for the new user
                _ = await self.notification.create(
                    db,
                    CreateNotificationSchema(
                        title=NOTIF_TITLE,
                        message=NOTIF_MESSAGE,
                        user_id=new_user.id
                    )
                )
                return token, url

            token = await self.__generate_token(user)
            url = f"{app_configs.FRONTEND_URL}/oauth-success"
            return token, url
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))

    async def rate_user(self, db: Session, user_id: str, rating: int):
        try:
            user = await self.repo.attachDB(db).get_by_id(user_id)
            if not user:
                raise ExcRaiser404(message='User not found')
            rating_count = user.rating_count + 1
            rating_sum = user.rating + rating
            rating = round(rating_sum / rating_count, 2)
            _ = await self.repo.attachDB(db).save(
                user,
                {
                    'rating': rating,
                    'rating_count': rating_count
                }
            )
            return True
        except ExcRaiser as e:
            raise
        except Exception as e:
            if self.debug:
                method_name = inspect.stack()[0].frame.f_code.co_name
                print(f"Unexpected error in {method_name}: {e}")
            raise ExcRaiser500(detail=str(e))
