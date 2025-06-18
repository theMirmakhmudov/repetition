from aiogram.fsm.state import StatesGroup, State

class ApplicationForm(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    phone_number = State()
    address = State()
    application_type = State()
    application_description = State()