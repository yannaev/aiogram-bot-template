from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminKeyboards:
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Get user", callback_data="get_user")],
                [InlineKeyboardButton(text="Block user", callback_data="block_user")],
                [InlineKeyboardButton(text="Unblock user", callback_data="unblock_user")],
            ]
        )
