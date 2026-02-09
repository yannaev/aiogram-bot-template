from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def hello_world(message: Message) -> None:
    await message.answer("Hello world!")
