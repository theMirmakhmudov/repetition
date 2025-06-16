from aiogram import Dispatcher
from handlers import start, help, register_student


def register_all_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(register_student.router)
