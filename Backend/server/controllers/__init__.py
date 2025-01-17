from fastapi import APIRouter
from server.config import app_configs
from server.controllers.user_controller import route as user_route
from server.controllers.category_controller import route as cat_route
from server.controllers.category_controller import sub_route
from server.controllers.items_controller import route as item_route
from server.controllers.auction_controller import route as auction_route


routes = APIRouter(prefix=app_configs.URI_PREFIX)

routes.include_router(user_route)
routes.include_router(cat_route)
routes.include_router(sub_route)
routes.include_router(item_route)
routes.include_router(auction_route)