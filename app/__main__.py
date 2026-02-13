import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.database.session import async_session_maker
from app.handlers.admin import admin_router
from app.handlers.start import start_router
from app.middlewares.database import DBMiddleware
from app.middlewares.subscription import SubscriptionMiddleware


async def main() -> None:
    dp = Dispatcher()

    dp.include_routers(start_router, admin_router)

    dp.update.middleware(DBMiddleware(session_factory=async_session_maker))

    dp.message.middleware(SubscriptionMiddleware(channel_id=settings.channel_id, channel_url=settings.channel_url))
    dp.callback_query.middleware(SubscriptionMiddleware(channel_id=settings.channel_id, channel_url=settings.channel_url))

    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
