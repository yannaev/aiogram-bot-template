from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class UserKeyboards:
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Pay", callback_data="payment")],
                [InlineKeyboardButton(text="Referral", callback_data="referral")],
                [InlineKeyboardButton(text="Support", callback_data="support")],
            ]
        )
