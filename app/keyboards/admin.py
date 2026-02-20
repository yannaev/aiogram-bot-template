from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminKeyboards:
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Get user", callback_data="get_user")],
            [InlineKeyboardButton(text="Block user", callback_data="block_user")],
            [InlineKeyboardButton(text="Unblock user", callback_data="unblock_user")],
        ]
    )

    back_to_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back", callback_data="admin")],
        ]
    )
