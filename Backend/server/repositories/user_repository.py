from server.repositories.repository import Repository
from server.models.users import Users, Notifications
from server.schemas.user_schema import GetUserSchema


class UserRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Users)

    async def get_by_email(
            self, email: str, schema_mode: bool = False
        ) -> GetUserSchema | Users:
        user = await self.get_by_attr({'email': email})
        if user and schema_mode:
            user = GetUserSchema.model_validate(user)
            return user
        elif user and not schema_mode:
            return user
        return None
    
    async def get_by_username(
            self, username: str, schema_mode: bool = False
        ) -> GetUserSchema | Users:
        user = await self.get_by_attr({'username': username})
        if user and schema_mode:
            user = GetUserSchema.model_validate(user)
            return user
        elif user and not schema_mode:
            return user
        return None
    

class UserNotificationRepository(Repository):
    def __init__(self, db):
        super().__init__(db, Notifications)