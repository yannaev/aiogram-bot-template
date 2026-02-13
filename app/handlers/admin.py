from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import settings
from app.middlewares.admin import AdminMiddleware

admin_router = Router()
admin_middleware = AdminMiddleware(admin_ids=settings.admin_ids)
admin_router.message.middleware(admin_middleware)
admin_router.callback_query.middleware(admin_middleware)


@admin_router.message(Command("admin"))
async def admin(message: Message) -> None:
    await message.answer("Menu for admin")
