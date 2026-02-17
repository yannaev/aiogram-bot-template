from app.exceptions.exceptions import ObjectAlreadyExistsException
from app.schemas.user import UserDTO, UserCreateDTO
from app.services.base import BaseService


class UserService(BaseService):
    async def get_or_create(self, telegram_id: int, referrer_id: int | None = None) -> UserDTO:
        user = await self.db.user.get_one_or_none(telegram_id=telegram_id)

        if user:
            return user

        if referrer_id:
            if referrer_id == telegram_id:
                referrer_id = None
            else:
                referrer = await self.db.user.get_one_or_none(telegram_id=referrer_id)
                if referrer is None:
                    referrer_id = None

        user_schema = UserCreateDTO(telegram_id=telegram_id, referrer_telegram_id=referrer_id)

        try:
            user = await self.db.user.create(data=user_schema)
            await self.db.commit()

        except ObjectAlreadyExistsException:
            await self.db.session.rollback()
            user = await self.db.user.get_one(telegram_id=telegram_id)

        return user
