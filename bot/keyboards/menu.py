from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сделать запись")],
        [KeyboardButton(text="Данные"),
        KeyboardButton(text="Настройки")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)
