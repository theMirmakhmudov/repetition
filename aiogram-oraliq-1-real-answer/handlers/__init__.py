from aiogram import Dispatcher
from handlers import start, about, contact, application


def register_all_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(about.router)
    dp.include_router(contact.router)
    dp.include_router(application.router)
