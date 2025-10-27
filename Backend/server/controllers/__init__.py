from fastapi import APIRouter
from server.config import app_configs
from server.controllers.user_controller import route as user_route
from server.controllers.category_controller import route as cat_route
from server.controllers.category_controller import sub_route
from server.controllers.items_controller import route as item_route
from server.controllers.auction_controller import route as auction_route
from server.controllers.bid_controller import route as bid_route
from server.controllers.misc_controller import route as misc_route
from server.controllers.landing_page_controller import (
    router as landing_page_router
)
from server.blog.blogController import route as blog_route


routes = APIRouter(prefix=app_configs.URI_PREFIX)

auction_route.include_router(bid_route)

routes.include_router(user_route)
routes.include_router(cat_route)
routes.include_router(sub_route)
routes.include_router(item_route)
routes.include_router(auction_route)
routes.include_router(misc_route)
routes.include_router(landing_page_router)
routes.include_router(blog_route)