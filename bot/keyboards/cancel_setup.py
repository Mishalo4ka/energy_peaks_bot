from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отменить настройку")]
    ],
    resize_keyboard=True
)
