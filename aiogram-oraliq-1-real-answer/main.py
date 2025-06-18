import asyncio
import logging
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from handlers import register_all_handlers

dp = Dispatcher()

async def main() -> None:
    bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    register_all_handlers(dp)
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
