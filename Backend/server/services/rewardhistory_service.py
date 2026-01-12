from server.schemas import PagedResponse, RewardHistoryQuery, RewardHistorySchema
from server.schemas.user_schema import CreateNotificationSchema
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser404, ExcRaiser500
from server.utils.ex_inspect import ExtInspect
from server.config import app_configs
from server.services.base_service import BaseService


class RewardHistoryService(BaseService):

    def __init__(self, repository, user_repository, notification_service):
        self.repo = repository
        self.user_repo = user_repository
        self.notification_service = notification_service

        self.debug = app_configs.DEBUG
        self.inspect = ExtInspect(self.__class__.__name__).info
        self.rewards_config = app_configs.rewards

    async def get_reward_amount(self, reward_type: str) -> int:
        reward_type = reward_type.upper()
        reward_amount = getattr(self.rewards_config, reward_type, 0)
        return reward_amount

    async def save_reward_history(self, user_id, reward_type):
        try:
            reward_type = reward_type.upper()
            reward_amount = await self.get_reward_amount(reward_type)
            reward_data = {
                "user_id": user_id,
                "amount": reward_amount,
                "type": reward_type,
            }
            reward_record = await self.repo.add(reward_data)
            _ = await self.user_repo.set_bid_points(user_id, reward_amount)

            # Notify user of reward
            notif_title = "You've earned reward points!"
            notif_message = f"You have been awarded {reward_amount} bid points for {reward_type.replace('_', ' ').title()}."
            notif_links = ["/dashboard/"]
            notif_class_name = "RewardNotification"
            _ = await self.notification_service.create(
                db=None,
                data=CreateNotificationSchema(
                    title=notif_title,
                    message=notif_message,
                    user_id=user_id,
                    links=notif_links,
                    class_name=notif_class_name,
                ),
            )
            return reward_record
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.DEBUG:
                self.inspect()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

    async def redeem_reward_points(self, user_id, points):
        try:
            user = await self.user_repo.redeem_bid_points(user_id, points)
            return user
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.DEBUG:
                self.inspect()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))

    async def get_user_reward_history(self, user_id, filter: RewardHistoryQuery):
        try:
            # rewards
            filter_params = filter.model_dump(exclude_unset=True, exclude_none=True)
            filter_params["user_id"] = user_id
            result: PagedResponse = await self.repo.get_all(filter_params)
            if not result:
                raise ExcRaiser404(message="No Reward History found")
            rewards = [
                RewardHistorySchema.model_validate(reward).model_dump()
                for reward in result.data
            ]
            result.data = rewards
            return result
        except ExcRaiser as e:
            raise e
        except Exception as e:
            if self.config.DEBUG:
                self.inspect()
                raise ExcRaiser500(detail=str(e), exception=e)
            raise ExcRaiser500(detail=str(e))
