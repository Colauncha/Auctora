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

from server.repositories import DBAdaptor

# from server.repositories.repository import Repository
from server.repositories.bid_repository import BidRepository
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


class Services:
    """
    A class that aggregates all services.
    This allows for easy access to all services from a single import.
    """
    # Repositories
    Plug = DBAdaptor()
    Plug.user_repo = UserRepository
    Plug.item_repo = ItemRepository
    Plug.category_repo = CategoryRepository
    Plug.sub_category_repo = SubCategoryRepository
    Plug.auction_repo = AuctionRepository
    Plug.auction_p_repo = AuctionParticipantRepository
    Plug.notif_repo = UserNotificationRepository
    Plug.bid_repo = BidRepository
    Plug.wallet_repo = WalletTranscationRepository
    Plug.payment_repo = PaymentRepository

    # Services
    contactUsServices = ContactUsService()
    notificationServices = UserNotificationServices(Plug.notif_repo)
    walletServices = UserWalletTransactionServices(
        Plug.notif_repo, Plug.user_repo, notificationServices
    )
    userServices = UserServices(Plug.user_repo, notificationServices)
    itemServices = ItemServices(Plug.item_repo, Plug.sub_category_repo)
    categoryServices = CategoryServices(
        Plug.category_repo, Plug.sub_category_repo
    )
    auctionServices = AuctionServices(
        Plug.auction_repo, Plug.auction_p_repo, Plug.user_repo,
        Plug.payment_repo, notificationServices
    )
    bidServices = BidServices(
        Plug.bid_repo, Plug.user_repo, Plug.auction_repo,
        notificationServices, auctionServices
    )

    @staticmethod
    def get_from_cookie(request: Request):
        token = request.cookies.get('access_token', None)
        return token
    
    @staticmethod
    async def get_ws_user(ws: WebSocket, db: Session = Depends(get_db), token = None):
        try:
            if token:
                user = await UserServices._get_current_user(token, db)
                return user
            else:
                token = ws.headers.get('Authorization')
                token = token.split(' ')[-1] if token else None
                return await UserServices._get_current_user(token, db)
        except:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    @staticmethod
    async def _get_current_user(
        token: Annotated[str, Depends(oauth_bearer), Depends(get_from_cookie)],
        db: Session = Depends(get_db)
    ) -> GetUserSchema:
        repo = Services.Plug.user_repo
        try:
            if not token:
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

Services = Services()
current_user = Annotated[GetUserSchema, Depends(Services._get_current_user)]
