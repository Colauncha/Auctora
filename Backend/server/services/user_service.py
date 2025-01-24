from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JWTError, JWTClaimsError
from passlib.context import CryptContext
from server.config import app_configs, redis_store
from server.config.database import get_db
from server.schemas import (
    VerifyOtpSchema, LoginSchema,
    GetUserSchema, UpdateUserSchema,
    LoginToken, ResetPasswordSchema,
    ChangePasswordSchema, PagedResponse,
    PagedQuery, GetUsers
)
from server.repositories import DBAdaptor
from server.models.users import Users
from server.middlewares.exception_handler import (
    ExcRaiser, ExcRaiser404, ExcRaiser500, ExcRaiser400
)
from server.utils import (
    is_valid_email, otp_generator,
    publish_otp, publish_reset_token
)
from sqlalchemy.orm import Session
from uuid import uuid4


oauth_bearer = OAuth2PasswordBearer(tokenUrl=f"api/users/login")


class UserServices:
    def __init__(self, db: Session):
        self.repo = DBAdaptor(db).user_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __check_password(self, password, hashed_password) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    async def __generate_token(self, user: Users) -> LoginToken:
        expires_at = datetime.now(tz=timezone.utc) + timedelta(
            days=app_configs.security.ACCESS_TOKEN_EXPIRES
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

    async def authenticate(self, identity: LoginSchema) -> LoginToken:
        try:
            user = None
            if is_valid_email(identity.identifier):
                user = await self.repo.get_by_email(identity.identifier)
            else:
                user = await self.repo.get_by_username(identity.identifier)
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
        except Exception as e:
            if type(e) == ExcRaiser:
                raise e
            raise ExcRaiser(
                status_code=401,
                message='Unauthorized',
                detail=e.__repr__()
            )

    async def create_user(self, data: dict) -> dict[str, str]:
        try:
            # Check if email already exist
            exist_user_email = await self.repo.get_by_email(
                data.get('email')
            )
            if exist_user_email:
                raise ExcRaiser(
                    message="Email already in use",
                    status_code=400,
                    detail="Use another email address or login with the email"
                )

            # Check if username already exist
            exist_user_username = await self.repo.get_by_username(
                data.get('username')
            )
            if exist_user_username:
                raise ExcRaiser(
                    message="Username already in use",
                    status_code=400,
                    detail="Use another username address or login with the username"
                )

            # Create new user
            else:
                new_user = await self.repo.add(data)
                if not new_user:
                    raise ExcRaiser(
                        message="Unable to create User",
                        status_code=400,
                        detail="Unable to create User"
                    )

                new_user = GetUserSchema.model_validate(new_user)
                otp = otp_generator()
                async_redis = await redis_store.get_async_redis()
                _ = await async_redis.set(f'otp:{new_user.email}', otp, ex=1800)
                # url = f"http://link.to.frontend/verify_otp?id={id}&otp={otp}"

                return {
                    'email': new_user.email,
                    'otp': otp,
                    # 'url': url,
                }

        except Exception as e:
            if type(e) == ExcRaiser:
                raise e
            raise ExcRaiser(
                message="Unable to create User",
                status_code=400,
                detail=str(e)
            )

    # async def create_admin(self, data: dict):
    #     try:
    #         ex_uname = await self.repo.get_by_username(data.get('username'))
    #         ex_email = await self.repo.get_by_username(data.get('email'))
    #         if ex_email or ex_uname:
    #             raise Exception()
    #     except Exception as e:
    #         ...

    async def retrieve(self, id) -> GetUserSchema:
        try:
            user = await self.repo.get_by_attr({'id': id})
            if user:
                valid_user = GetUserSchema.model_validate(user)
                return valid_user
            raise ExcRaiser404(message='User not found')
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser(
                message="Unable to Fetch User",
                status_code=400,
                detail=str(e)
            )
        
    async def list(self, filter: PagedQuery) ->PagedResponse[list[GetUsers]]:
        try:
            result = await self.repo.get_all(filter.model_dump(exclude_unset=True))
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
        except Exception as e:
            raise e
        
    async def new_otp(self, email: str):
        try:
            async_redis = await redis_store.get_async_redis()
            stored_otp = await async_redis.get(f'otp:{email}')
            if stored_otp:
                _ = await async_redis.delete(f'otp:{email}')
            user = await self.repo.get_by_email(email)
            if user.email_verified:
                return {'detail': 'User email already verified'}
            otp = otp_generator()
            _ = await async_redis.set(f'otp:{email}', otp, ex=1800)
            data = {'email': email, 'otp': otp}
            await publish_otp(data)
            return {'detail': 'OTP resent to Email'}
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser500()

    async def verify_otp(self, data: VerifyOtpSchema):
        try:
            async_redis = await redis_store.get_async_redis()
            stored_otp = await async_redis.get(f'otp:{data.email}')
            user = await self.repo.get_by_email(data.email)
            if stored_otp == data.otp:
                _ = await self.repo.save(user, {'email_verified': True})
                _ = await async_redis.delete(f'otp:{data.email}')
                return {'message': 'email verified'}
            return {'message': 'Invalid otp or email'}
        except Exception as e:
            raise ExcRaiser(
                status_code=400,
                message='Unable to verify email',
                detail=e.__repr__()
            )

    async def update_user(self, user: GetUserSchema, data: UpdateUserSchema):
        try:
            if not user:
                raise HTTPException(
                    status_code=400, detail="Not authenticated"
                )
            _data = data.model_dump(exclude_unset=True, exclude_none=True)
            result = await self.repo.update(user, _data)
            if result:
                return True
        except (HTTPException, Exception) as exc:
            raise ExcRaiser(
                status_code=getattr(exc, 'status_code', 400),
                message="Update not successful",
                detail=exc.__repr__()
            )
        
    async def get_reset_token(self, email: str):
        try:
            user = await self.repo.get_by_email(email)
            if not user:
                raise ExcRaiser404("User not found")
            token = uuid4().hex
            async_redis = await redis_store.get_async_redis()
            _ = await async_redis.set(f'reset_password:{email}', token, ex=1800)
            data = {'email': email, 'token': token}
            await publish_reset_token(data)
            return {'detail': 'Reset token sent to email'}
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise e

    async def reset_password(self, data: ResetPasswordSchema):
        try:
            async_redis = await redis_store.get_async_redis()
            stored_token = await async_redis.get(f'reset_password:{data.email}')
            if stored_token == data.token: 
                if data.password == data.confirm_password:
                    user = await self.repo.get_by_email(data.email)
                    _ = await self.repo.save(
                        user, {'hash_password': self.pwd_context.hash(data.password)}
                    )
                    _ = await async_redis.delete(f'reset_password:{data.email}')
                    return {'detail': 'Password reset successful'}
                raise ExcRaiser400(detail='Passwords do not match')
            raise ExcRaiser400(detail= 'Invalid token or email')
        except Exception as e:
            if issubclass(type(e), ExcRaiser):
                raise e
            raise ExcRaiser500()
        
    async def change_password(self, user: GetUserSchema, data: ChangePasswordSchema):
        try:
            user = await self.repo.get_by_email(user.email)
            if not self.__check_password(data.old_password, user.hash_password):
                raise ExcRaiser400(detail='Invalid old password')
            if data.new_password == data.confirm_password:
                _ = await self.repo.save(
                    user, {'hash_password': self.pwd_context.hash(data.new_password)}
                )
                return {'detail': 'Password change successful'}
            raise ExcRaiser400(detail='Passwords do not match')
        except Exception as exc:
            print(exc)
            if issubclass(type(exc), ExcRaiser):
                raise exc
            raise ExcRaiser500()

    @staticmethod
    async def _get_current_user(
        token: Annotated[str, Depends(oauth_bearer)],
        db: Session = Depends(get_db)
    ) -> GetUserSchema:
        repo = UserServices(db).repo
        try:
            claims = jwt.decode(
                token=token,
                algorithms=app_configs.security.ALGORITHM,
                key=app_configs.security.JWT_SECRET_KEY
            )
            if claims and claims.get('email') and claims.get('id'):
                user = await repo.get_by_attr({'id': claims.get('id')})
                if user:
                    return GetUserSchema.model_validate(user)
            else:
                raise ExcRaiser(
                    status_code=401,
                    message = 'Unauthorized',
                    detail="Invalid token"
                )
        except ExpiredSignatureError as ex_sig:
            raise ExcRaiser(
                status_code=401,
                message='Unauthorized',
                detail=['Expired token', ex_sig.__repr__()]
            )
        except (JWTClaimsError, JWTError) as j_e:
            raise ExcRaiser(
                status_code=401,
                message='Unauthorized',
                detail=['Invalid token', j_e.__repr__()]
            )
        except Exception as e:
            if type(e) == ExcRaiser:
                raise e
            raise ExcRaiser(
                status_code=401,
                message='Unauthorized',
                detail=e.__repr__()
            )
        

current_user = Annotated[GetUserSchema, Depends(UserServices._get_current_user)]
