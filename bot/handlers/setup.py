from datetime import datetime

from aiogram import F, Router, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import menu, cancel_setup

from states import Setup


router = Router()


@router.message(StateFilter(Setup), F.text == "Отменить настройку")
async def cancel_settings(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Настройка отменена",
        reply_markup=menu
    )


@router.message(F.text == "Настройки")
async def settings_start(message: Message, state: FSMContext):
    await state.set_state(Setup.waiting_for_timezone)
    await message.answer(
        f"{html.bold('Введите ваш часовой пояс:')}\nПример: +7 для Москвы",
        reply_markup=cancel_setup
    )


@router.message(Setup.waiting_for_timezone)
async def set_timezone(message: Message, state: FSMContext):
    try:
        timezone = int(message.text.strip())
    except ValueError:
        await message.answer("Введите целое число.\nНапример: 2 или -3")
        return

    if not -12 <= timezone <= 14:
        await message.answer("Смещение должно быть в диапазоне от -12 до +14")
        return

    await state.update_data(timezone=timezone)
    await state.set_state(Setup.waiting_for_notification_start)

    await message.answer(f"{html.bold('Введите время начала уведомлений:')}\nНапример: 09:00")


@router.message(Setup.waiting_for_notification_start)
async def set_notification_start(message: Message, state: FSMContext):
    try:
        start_time = datetime.strptime(message.text.strip(), "%H:%M").time()
    except ValueError:
        await message.answer("Неверный формат.\nИспользуйте HH:MM")
        return

    await state.update_data(notification_start=start_time)
    await state.set_state(Setup.waiting_for_notification_end)

    await message.answer(
        f"{html.bold('Введите время окончания уведомлений:')}\nНапример: 21:00",
    )


@router.message(Setup.waiting_for_notification_end)
async def set_notification_end(message: Message, state: FSMContext):
    try:
        end_time = datetime.strptime(message.text.strip(), "%H:%M").time()
    except ValueError:
        await message.answer("Неверный формат.\nИспользуйте HH:MM")
        return

    data = await state.get_data()

    timezone = data["timezone"]
    start_time = data["notification_start"]

    if start_time == end_time:
        await message.answer("Начало и конец не могут совпадать.")
        return

    await message.answer(
        f"{html.bold('Настройки сохранены:')}\nЧасовой пояс: {timezone:+d}\nОкно уведомлений: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}",
        reply_markup=menu
    )

    await state.clear()
