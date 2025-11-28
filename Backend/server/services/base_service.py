from fastapi import HTTPException

from server.config.database import get_db
from server.config.app_configs import app_configs
from server.repositories import get_db_repo, Repository
from server.utils.ex_inspect import ExtInspect
from server.middlewares.exception_handler import ExcRaiser500


class BaseService:
    inspect = ExtInspect(
        class_name='BaseService'
    ).info
    config = app_configs

    @classmethod
    async def get_ownership(cls, model, id, user_id) -> bool:
        try:
            repo: Repository = get_db_repo()
            repo = repo(model)
            db = get_db()
            entity = await repo.attachDB(next(db)).get_by_id(id)

            if not entity:
                raise HTTPException(status_code=404, detail="Item not found")

            is_owner = False

            if getattr(entity, 'users_id', None) == user_id:
                is_owner = True
            elif getattr(entity, 'user_id', None) == user_id:
                is_owner = True
            elif getattr(entity, 'seller_id', None) == user_id:
                is_owner = True
            elif getattr(entity, 'buyer_id', None) == user_id:
                is_owner = True
            elif entity.id == user_id:
                is_owner = True

            return is_owner
        except Exception as e:
            if cls.config.DEBUG:
                cls.inspect()
                ExcRaiser500(e)
            ExcRaiser500(e)
