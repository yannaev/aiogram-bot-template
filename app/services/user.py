from app.exceptions.exceptions import ObjectAlreadyExistsException
from app.schemas.user import User, UserCreate
from app.services.base import BaseService


class UserService(BaseService):
    async def register(self, telegram_id: int) -> User:
        user_schema = UserCreate(telegram_id=telegram_id)

        try:
            user = await self.db.user.create(data=user_schema)
            await self.db.commit()
            return user
        except ObjectAlreadyExistsException:
            return await self.db.user.get_one(telegram_id=telegram_id)