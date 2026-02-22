from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ]
)
