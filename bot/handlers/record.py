from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import concentration_assessment, energy_assessment
from states import EnergyAssessment


router = Router()


@router.message(F.text == "Сделать запись")
async def record_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(EnergyAssessment.waiting_for_energy_assessment)
    
    await message.answer(
        f"{html.bold('Оцените количество энергии за последний час:')}\n", reply_markup=energy_assessment)


@router.callback_query(EnergyAssessment.waiting_for_energy_assessment)
async def rate_energy(callback: CallbackQuery, state: FSMContext):
    energy_score = int(callback.data.split("_")[1])
    
    await state.update_data(energy_assessment=energy_score)
    await state.set_state(EnergyAssessment.waiting_for_concentration_assessment)
    
    await callback.message.edit_text(
        f"{html.bold('Получены оценки:')}\nЭнергия: {energy_score}\n\n{html.bold('Теперь оцените концентрацию за последний час:')}",
        reply_markup=concentration_assessment,
    )
    
    await callback.answer()


@router.callback_query(EnergyAssessment.waiting_for_concentration_assessment)
async def rate_concentration(callback: CallbackQuery, state: FSMContext):
    concentration_score = int(callback.data.split("_")[1])
    
    await state.update_data(concentration_assessment=concentration_score)
    data = await state.get_data()
    energy_score = data.get("energy_assessment")
    
    await state.set_state(EnergyAssessment.waiting_for_employment_type)
    
    await callback.message.edit_text(
        f"{html.bold('Получены оценки:')}\nЭнергия: {energy_score}\nКонцентрация: {concentration_score}\n\n{html.bold('Укажите категорию деятельности (ответ текстом):')}"
    )
    
    await callback.answer()


@router.message(EnergyAssessment.waiting_for_employment_type)
async def get_employment_type(message: Message, state: FSMContext):
    employment_type = message.text

    data = await state.get_data()
    energy_score = data.get("energy_assessment")
    concentration_score = data.get("concentration_assessment")

    await message.answer(
        f"{html.bold('Получены оценки:')}\nЭнергия: {energy_score}\nКонцентрация: {concentration_score}\nКатегория: {employment_type}"
    )

    await state.clear()
