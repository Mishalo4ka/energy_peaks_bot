from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"{i}", callback_data=f"concentration_{i}")] for i in range(1, 6)
    ] + [[InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
)
