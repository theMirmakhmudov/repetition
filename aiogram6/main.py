import asyncio
import logging
import os

from aiogram import Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from db import Database

dp = Dispatcher()
db = Database(
    db_name=os.getenv("DB_NAME"),
    db_user=os.getenv("DB_USER"),
    db_password=os.getenv("DB_PASSWORD"),
    db_host=os.getenv("DB_HOST"),
    db_port=os.getenv("DB_PORT")
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if not db.exist_user(message.from_user.id):
        await message.answer(f"<b>Assalomu Aleykum, Xurmatli {message.from_user.mention_html()}</b>")
        db.add_user(message.from_user.full_name, message.from_user.username, message.from_user.id)
        return

    await message.answer(f"<b>Qaytganingiz bilan, {message.from_user.mention_html()}</b>")


async def main() -> None:
    bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    # logging.basicConfig(filename='aiogram6app.log', level=logging.DEBUG,
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.run(main())
