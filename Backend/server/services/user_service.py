from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JWTError, JWTClaimsError
from passlib.context import CryptContext
from server.config import app_configs, get_db, redis_store
from server.schemas import (
    ServiceResultModel,
    GetUserSchema,
    LoginSchema,
    LoginToken,
)
from server.repositories import DBAdaptor
from server.models.users import Users
from server.middlewares.exception_handler import ExcRaiser
from server.utils import is_valid_email, otp_generator, Emailer
from sqlalchemy.orm import Session


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
