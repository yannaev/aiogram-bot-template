from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import TelegramObject, User


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, channel_id: str, channel_url: str) -> None:
        self.channel_id = channel_id
        self.channel_url = channel_url

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        bot: Bot = data["bot"]

        try:
            member = await bot.get_chat_member(chat_id=self.channel_id, user_id=user.id)

            if member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
                    await event.answer(
                        "Need to subscribe channel\n"
                        f"{self.channel_url}"
                    )
                    return None
        except Exception:
            return await handler(event, data)

        return await handler(event, data)
