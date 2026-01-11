from server.utils.ex_inspect import ExtInspect
from server.config import app_configs
from server.services.base_service import BaseService


class RewardHistoryService(BaseService):
    def __init__(self, repository):
        self.repo = repository

        self.debug = app_configs.DEBUG
        self.inspect = ExtInspect(self.__class__.__name__).info
