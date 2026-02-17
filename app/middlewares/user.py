from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from app.schemas.user import UserDTO
from app.services.user import UserService


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        tg_user: User | None = data.get("event_from_user")
        db = data.get("db")

        if tg_user is None or db is None:
            return await handler(event, data)

        user: UserDTO = await UserService(db).get_or_create(telegram_id=tg_user.id)

        data["user"] = user

        return await handler(event, data)
