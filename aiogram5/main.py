import asyncio
import logging
from aiogram import Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from db import Database

dp = Dispatcher()
db = Database("users.db")


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
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
