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
@admin_router.callback_query(F.data == "admin")
async def admin_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = "Admin Menu"

    if isinstance(event, Message):
        await event.answer(text, reply_markup=AdminKeyboards.menu)
    else:
        await event.answer()
        await event.message.edit_text(text, reply_markup=AdminKeyboards.menu)


@admin_router.callback_query(F.data.in_({"get_user", "block_user", "unblock_user"}))
async def waiting_for_telegram_id(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.update_data(action=callback.data)
    await state.set_state(AdminStates.waiting_for_telegram_id)
    await callback.message.edit_text("Send telegram_id", reply_markup=AdminKeyboards.back_to_menu)


@admin_router.message(AdminStates.waiting_for_telegram_id)
async def process_telegram_id(message: Message, state: FSMContext, db: DBManager) -> None:
    if not message.text.isdigit():
        await message.answer(
            "Only numbers are allowed. Try again.", reply_markup=AdminKeyboards.back_to_menu
        )
        return

    telegram_id = int(message.text)
    state_data = await state.get_data()
    action = state_data.get("action")

    user = None
    text = ""

    match action:
        case "get_user":
            user = await UserService(db).get_one_or_none(telegram_id=telegram_id)
            if user:
                text = f"<pre><code class='language-json'>{user.model_dump_json(indent=4)}</code></pre>"
        case "block_user":
            user = await UserService(db).block(telegram_id=telegram_id)
            text = "Success. User has been blocked."
        case "unblock_user":
            user = await UserService(db).unblock(telegram_id=telegram_id)
            text = "Success. User has been unblocked."
        case _:
            await message.answer("Unknown action.", reply_markup=AdminKeyboards.back_to_menu)
            await state.clear()
            return

    if user:
        await message.answer(text=text, reply_markup=AdminKeyboards.back_to_menu)
    else:
        await message.answer("User not found.", reply_markup=AdminKeyboards.back_to_menu)

    await state.clear()
