from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.middlewares.admin import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())
admin_router.callback_query.middleware(AdminMiddleware())


@admin_router.message(Command("admin"))
async def admin(message: Message) -> None:
    await message.answer("Menu for admin")
