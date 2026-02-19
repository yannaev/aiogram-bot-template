from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from app.schemas.user import UserDTO
from app.services.user import UserService
from app.utils.deep_link import DeepLink


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

        referrer_telegram_id: int | None = None

        if event.message and event.message.text and event.message.text.startswith("/start ") and len(event.message.text) > 7:
            try:
                encoded_arg = event.message.text.split()[1]
                referrer_telegram_id = DeepLink.decode(encoded_arg)

            except (IndexError, ValueError):
                pass

        user: UserDTO = await UserService(db).get_or_create(telegram_id=tg_user.id, referrer_telegram_id=referrer_telegram_id)

        if user.is_blocked:
            return None

        data["user"] = user

        return await handler(event, data)
