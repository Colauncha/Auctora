from fastapi import APIRouter
from server.config import app_configs
from server.controllers.user_controller import route as user_route
from server.controllers.category_controller import route as cat_route
from server.controllers.category_controller import sub_route


router = APIRouter(prefix=app_configs.URI_PREFIX)

router.include_router(user_route)
router.include_router(cat_route)
router.include_router(sub_route)