from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.user import UserKeyboards
from app.schemas.user import UserDTO

start_router = Router()


@start_router.message(CommandStart())
async def main_menu(message: Message, user: UserDTO) -> None:
    await message.answer(f"<b>ID:</b> {user.telegram_id}", reply_markup=UserKeyboards.main_menu())
