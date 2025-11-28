from typing import Annotated
from fastapi import Depends, Request, WebSocket, WebSocketException, status
from jose import ExpiredSignatureError
from jose.exceptions import JWTError, JWTClaimsError
from server.config.database import get_db
from server.services.auction_service import AuctionServices
from server.services.bid_services import BidServices
from server.services.misc_service import ContactUsService
from server.services.user_service import *
from server.services.item_service import *
from server.services.category_service import *
from server.blog.blogService import BlogService
from server.chat.chatServices import ChatServices

from server.repositories import *

from server.blog.blogRepo import BlogRepository, BlogCommentRepository
from server.repositories.bid_repository import BidRepository
from server.chat.chatRepo import ChatRepository
from server.repositories.payment_repository import PaymentRepository
from server.repositories.auction_repository import (
    AuctionRepository, AuctionParticipantRepository
)
from server.repositories.item_repository import (
    ItemRepository, CategoryRepository,
    SubCategoryRepository
)
from server.repositories.user_repository import (
    UserRepository, UserNotificationRepository,
    WalletTranscationRepository
)


# Service dependencies
def get_contact_us_service():
    return ContactUsService()


def get_notification_service(
    notification_repo: UserNotificationRepository = Depends(
        get_notification_repo
    )
):
    return UserNotificationServices(notification_repo)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
    notification_service: UserNotificationServices = Depends(
        get_notification_service
    )
):
    return UserServices(user_repo, notification_service)


def get_wallet_service(
    wallet: WalletTranscationRepository = Depends(get_wallet_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    notification_service: UserNotificationServices = Depends(
        get_notification_service
    )
):
    return UserWalletTransactionServices(wallet, user_repo, notification_service)


def get_chat_service(
    chat_repo: ChatRepository = Depends(get_chat_repo)
):
    return ChatServices(chat_repo)


def get_item_service(
    item_repo: ItemRepository = Depends(get_item_repo),
    sub_cat_repo: SubCategoryRepository = Depends(
        get_sub_category_repo
    )
):
    return ItemServices(item_repo, sub_cat_repo)


def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repo),
    sub_cat_repo: SubCategoryRepository = Depends(
        get_sub_category_repo
    )
):
    return CategoryServices(category_repo, sub_cat_repo)


def get_auction_service(
    auction_repo: AuctionRepository = Depends(get_auction_repo),
    auction_p_repo: AuctionParticipantRepository = Depends(
        get_auction_p_repo
    ),
    user_repo: UserRepository = Depends(get_user_repo),
    payment_repo: PaymentRepository = Depends(get_payment_repo),
    notification_service: UserNotificationServices = Depends(
        get_notification_service
    ),
    chat_service: ChatServices = Depends(get_chat_service)
):
    return AuctionServices(
        auction_repo, auction_p_repo,
        user_repo, payment_repo, notification_service,
        chat_service
    )


def get_bid_service(
    bid_repo: BidRepository = Depends(get_bid_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    auction_repo: AuctionRepository = Depends(get_auction_repo),
    notification_service: UserNotificationServices = Depends(
        get_notification_service
    ),
    auction_service: AuctionServices = Depends(get_auction_service)
):
    return BidServices(
        bid_repo, user_repo, auction_repo,
        notification_service, auction_service
    )


def get_blog_service(
    blog_repo: BlogRepository = Depends(get_blog_repo),
    blog_comment_repo: BlogCommentRepository = Depends(
        get_blog_comment_repo
    )
):
    return BlogService(blog_repo, blog_comment_repo)


# Auth related services and dependencies
class AuthServices:
    from fastapi.security import OAuth2PasswordBearer

    oauth_bearer = OAuth2PasswordBearer(tokenUrl=f"api/users/login")

    @staticmethod
    def get_from_cookie(request: Request):
        token = request.cookies.get('access_token', None)
        return token
    
    # @staticmethod
    # async def get_ws_user(
    #     ws: WebSocket,
    #     db: Session = Depends(get_db),
    #     token = None,
    #     user_repo: UserRepository = Depends(get_user_repo),
    # ):
    #     try:
    #         if not token:
    #             token = ws.headers.get('Authorization')
    #             token = token.split(' ')[-1] if token else None

    #         claims = jwt.decode(
    #             token=token,
    #             algorithms=app_configs.security.ALGORITHM,
    #             key=app_configs.security.JWT_SECRET_KEY
    #         )

    #         if claims and claims.get('email') and claims.get('id'):
    #             user = await user_repo.attachDB(db).get_by_attr({'id': claims.get('id')})
    #             print(user)
    #             if user:
    #                 return GetUserSchema.model_validate(user)
    #     except:
    #         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    @staticmethod
    async def get_ws_user(ws: WebSocket):
        try:
            token = ws.headers.get('Authorization')
            if token:
                token = token.split(' ')[-1]

            if not token:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

            claims = jwt.decode(
                token,
                app_configs.security.JWT_SECRET_KEY,
                algorithms=[app_configs.security.ALGORITHM]
            )

            # Get DB and repo manually (NOT via Depends)
            db = next(get_db())               # call generator
            user_repo = get_user_repo()   # if this returns a class/service

            user = await user_repo.attachDB(db).get_by_attr({'id': claims["id"]})

            if not user:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

            return GetUserSchema.model_validate(user)

        except WebSocketException:
            raise
        except Exception:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


    @staticmethod
    async def _get_current_user(
        token: Annotated[str, Depends(oauth_bearer), Depends(get_from_cookie)],
        user_repo: UserRepository = Depends(get_user_repo),
        db: Session = Depends(get_db),
    ) -> GetUserSchema:
        repo = user_repo
        try:
            if not token:
                raise ExcRaiser(
                    status_code=401,
                    message='Unauthenticated',
                    detail='No token provided'
                )

            async_redis = await redis_store.get_async_redis()
            blacklisted = await async_redis.get(f"blacklist_{token}")
            if blacklisted:
                raise ExcRaiser(
                    status_code=401,
                    message='Unauthenticated',
                    detail='No token provided'
                )

            claims = jwt.decode(
                token=token,
                algorithms=app_configs.security.ALGORITHM,
                key=app_configs.security.JWT_SECRET_KEY
            )

            if claims and claims.get('email') and claims.get('id'):
                user = await repo.attachDB(db).get_by_attr({'id': claims.get('id')})
                if user:
                    return GetUserSchema.model_validate(user)
            else:
                raise ExcRaiser(
                    status_code=401,
                    message = 'Unauthenticated',
                    detail="Invalid token"
                )
        except ExpiredSignatureError as ex_sig:
            raise ExcRaiser(
                status_code=401,
                message='Unauthenticated',
                detail=['Expired token', ex_sig.__repr__()]
            )
        except (JWTClaimsError, JWTError) as j_e:
            raise ExcRaiser(
                status_code=401,
                message='Unauthenticated',
                detail=['Invalid token', j_e.__repr__()]
            )
        except Exception as e:
            if type(e) == ExcRaiser:
                raise e
            raise ExcRaiser(
                status_code=401,
                message='Unauthenticated',
                detail=e.__repr__()
            )

    @staticmethod
    async def verify_token(
        request: Request,
    ) -> bool:
        try:
            token = request.cookies.get('access_token', None)
            if not token:
                return False

            async_redis = await redis_store.get_async_redis()
            blacklisted = await async_redis.get(f"blacklist_{token}")
            if blacklisted:
                return False

            claims = jwt.decode(
                token=token,
                algorithms=app_configs.security.ALGORITHM,
                key=app_configs.security.JWT_SECRET_KEY
            )

            if claims:
                return True
            return False
        except Exception:
            return False


current_user = Annotated[GetUserSchema, Depends(AuthServices._get_current_user)]
