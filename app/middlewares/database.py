from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any
from aiogram.types import TelegramObject

from app.database.manager import DBManager


class DBMiddleware(BaseMiddleware):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with DBManager(session_factory=self.session_factory) as db:
            data["db"] = db
            return await handler(event, data)
