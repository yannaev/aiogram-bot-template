from app.exceptions.exceptions import ObjectAlreadyExistsException
from app.schemas.user import UserDTO, UserCreateDTO, UserUpdateDTO
from app.services.base import BaseService


class UserService(BaseService):
    async def get_or_create(
        self, telegram_id: int, referrer_telegram_id: int | None = None
    ) -> UserDTO:
        user = await self.db.user.get_one_or_none(telegram_id=telegram_id)

        if user:
            return user

        if referrer_telegram_id:
            if referrer_telegram_id == telegram_id:
                referrer_telegram_id = None
            else:
                referrer = await self.db.user.get_one_or_none(telegram_id=referrer_telegram_id)
                if referrer is None:
                    referrer_telegram_id = None

        user_schema = UserCreateDTO(
            telegram_id=telegram_id, referrer_telegram_id=referrer_telegram_id
        )

        try:
            user = await self.db.user.create(data=user_schema)
            await self.db.commit()

        except ObjectAlreadyExistsException:
            await self.db.session.rollback()
            user = await self.db.user.get_one(telegram_id=telegram_id)

        return user

    async def get(self, telegram_id: int) -> UserDTO | None:
        return await self.db.user.get_one_or_none(telegram_id=telegram_id)

    async def block(self, telegram_id: int) -> UserDTO | None:
        return await self._update_status(telegram_id, is_blocked=True)

    async def unblock(self, telegram_id: int) -> UserDTO | None:
        return await self._update_status(telegram_id, is_blocked=False)

    async def _update_status(self, telegram_id: int, is_blocked: bool) -> UserDTO | None:
        data = UserUpdateDTO(is_blocked=is_blocked)

        user = await self.db.user.update(data=data, telegram_id=telegram_id)

        if user:
            await self.db.commit()

        return user
