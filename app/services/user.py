from app.exceptions.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from app.schemas.user import UserDTO, UserCreateDTO
from app.services.base import BaseService


class UserService(BaseService):
    async def get_or_create(self, telegram_id: int) -> UserDTO:
        try:
            user = await self.db.user.get_one(telegram_id=telegram_id)

        except ObjectNotFoundException:
            user_schema = UserCreateDTO(telegram_id=telegram_id)

            try:
                user = await self.db.user.create(data=user_schema)
                await self.db.commit()

            except ObjectAlreadyExistsException:
                await self.db.session.rollback()
                user = await self.db.user.get_one(telegram_id=telegram_id)

        return user

    async def create(self, telegram_id: int) -> UserDTO:
        user_schema = UserCreateDTO(telegram_id=telegram_id)

        try:
            user = await self.db.user.create(data=user_schema)
            await self.db.commit()
            return user
        except ObjectAlreadyExistsException:
            await self.db.session.rollback()
            return await self.db.user.get_one(telegram_id=telegram_id)
