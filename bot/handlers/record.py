from aiogram import F, Router, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import concentration_assessment, energy_assessment, menu, get_employment

from states import EnergyAssessment

from bot.database.session import AsyncSessionLocal
from bot.services.energy_service import EnergyService

router = Router()


@router.callback_query(StateFilter(EnergyAssessment), F.data == "cancel")
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Ввод данных отменён",
        reply_markup=menu
    )
    await callback.answer()
    

@router.message(F.text == "Сделать запись")
async def record_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(EnergyAssessment.waiting_for_energy_assessment)
    
    await message.answer(
        f"{html.bold('Оцените количество энергии за последний час:')}", reply_markup=energy_assessment)


@router.callback_query(
    EnergyAssessment.waiting_for_energy_assessment,
    F.data.startswith("energy_")
)
async def rate_energy(callback: CallbackQuery, state: FSMContext):
    energy_score = int(callback.data.split("_")[1])
    
    await state.update_data(energy_assessment=energy_score)
    await state.set_state(EnergyAssessment.waiting_for_concentration_assessment)
    
    await callback.message.edit_text(
        f"{html.bold('Получены оценки:')}\nЭнергия: {energy_score}\n\n{html.bold('Теперь оцените концентрацию за последний час:')}",
        reply_markup=concentration_assessment,)
    
    await callback.answer()


@router.callback_query(
    EnergyAssessment.waiting_for_concentration_assessment,
    F.data.startswith("concentration_")
)
async def rate_concentration(callback: CallbackQuery, state: FSMContext):
    concentration_score = int(callback.data.split("_")[1])

    await state.update_data(concentration_assessment=concentration_score)
    data = await state.get_data()
    energy_score = data["energy_assessment"]

    await state.set_state(EnergyAssessment.waiting_for_employment_type)

    await callback.message.edit_text(
        f"{html.bold('Получены оценки:')}\n"
        f"Энергия: {energy_score}\n"
        f"Концентрация: {concentration_score}\n\n"
        f"{html.bold('Укажите категорию деятельности:')}",
        reply_markup=get_employment
    )

    await callback.answer()


@router.message(EnergyAssessment.waiting_for_employment_type)
async def get_employment_type(message: Message, state: FSMContext):
    employment_type = message.text

    data = await state.get_data()
    energy_score = data.get("energy_assessment")
    concentration_score = data.get("concentration_assessment")

    try:
        async with AsyncSessionLocal() as session:
            await EnergyService.create_record(
                session=session,
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                energy=energy_score,
                concentration=concentration_score,
                activity=employment_type,
            )

    except Exception as e:
        await message.answer("Ошибка при сохранении данных.")
        await state.clear()
        raise e

    await message.answer(
        f"{html.bold('Получены оценки:')}\nЭнергия: {energy_score}\nКонцентрация: {concentration_score}\nКатегория: {employment_type}",
        reply_markup=menu
    )

    await state.clear()
