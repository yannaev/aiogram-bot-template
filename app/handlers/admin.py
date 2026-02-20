from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.config import settings
from app.database.manager import DBManager
from app.keyboards.admin import AdminKeyboards
from app.middlewares.admin import AdminMiddleware
from app.services.user import UserService
from app.states.admin import AdminStates

admin_router = Router()
admin_middleware = AdminMiddleware(admin_ids=settings.admin_ids)
admin_router.message.middleware(admin_middleware)
admin_router.callback_query.middleware(admin_middleware)


@admin_router.message(Command("admin"))
async def admin(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Admin Menu", reply_markup=AdminKeyboards.menu)


@admin_router.callback_query(F.data == "admin")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(text="Admin Menu", reply_markup=AdminKeyboards.menu)


@admin_router.callback_query(F.data == "get_user")
async def get_user(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(AdminStates.get_user)
    await callback.message.edit_text("Send telegram_id.", reply_markup=AdminKeyboards.back_to_menu)


@admin_router.message(AdminStates.get_user)
async def get_user_state(message: Message, state: FSMContext, db: DBManager) -> None:
    if not message.text.isdigit():
        await message.answer(
            "Only numbers are allowed. Try again.", reply_markup=AdminKeyboards.back_to_menu
        )
        return

    telegram_id = int(message.text)

    user = await UserService(db).get_one_or_none(telegram_id=telegram_id)

    if user:
        await message.answer(
            text=f"<pre><code class='language-json'>{user.model_dump_json(indent=4)}</code></pre>",
            reply_markup=AdminKeyboards.back_to_menu,
        )
    else:
        await message.answer("User not found.", reply_markup=AdminKeyboards.back_to_menu)

    await state.clear()


@admin_router.callback_query(F.data == "block_user")
async def block_user(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(AdminStates.block_user)
    await callback.message.edit_text("Send telegram_id.", reply_markup=AdminKeyboards.back_to_menu)


@admin_router.message(AdminStates.block_user)
async def block_user_state(message: Message, state: FSMContext, db: DBManager) -> None:
    if not message.text.isdigit():
        await message.answer(
            "Only numbers are allowed. Try again.", reply_markup=AdminKeyboards.back_to_menu
        )
        return

    telegram_id = int(message.text)

    user = await UserService(db).block(telegram_id=telegram_id)

    if user:
        await message.answer(
            text="Success. User has been blocked.",
            reply_markup=AdminKeyboards.back_to_menu,
        )
    else:
        await message.answer("User not found.", reply_markup=AdminKeyboards.back_to_menu)

    await state.clear()


@admin_router.callback_query(F.data == "unblock_user")
async def unblock_user(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(AdminStates.unblock_user)
    await callback.message.edit_text("Send telegram_id.", reply_markup=AdminKeyboards.back_to_menu)


@admin_router.message(AdminStates.unblock_user)
async def unblock_user_state(message: Message, state: FSMContext, db: DBManager) -> None:
    if not message.text.isdigit():
        await message.answer(
            "Only numbers are allowed. Try again.", reply_markup=AdminKeyboards.back_to_menu
        )
        return

    telegram_id = int(message.text)

    user = await UserService(db).unblock(telegram_id=telegram_id)

    if user:
        await message.answer(
            text="Success. User has been unblocked.",
            reply_markup=AdminKeyboards.back_to_menu,
        )
    else:
        await message.answer("User not found.", reply_markup=AdminKeyboards.back_to_menu)

    await state.clear()
