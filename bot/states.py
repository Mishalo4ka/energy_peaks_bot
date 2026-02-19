from aiogram.fsm.state import State, StatesGroup

class EnergyAssessment(StatesGroup):
    waiting_for_energy_assessment = State()
    waiting_for_concentration_assessment = State()
    waiting_for_employment_type = State()

