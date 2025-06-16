from aiogram.fsm.state import StatesGroup, State

class RegisterStudent(StatesGroup):
    first_name = State()
    last_name = State()
    grade = State()
    phone_number = State()
    location = State()