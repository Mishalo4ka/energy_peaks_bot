from aiogram.fsm.state import State, StatesGroup


class EnergyAssessment(StatesGroup):
    waiting_for_energy_assessment = State()
    waiting_for_concentration_assessment = State()
    waiting_for_employment_type = State()


class Setup(StatesGroup):
    waiting_for_timezone = State()
    waiting_for_notification_start = State()
    waiting_for_notification_end = State()
