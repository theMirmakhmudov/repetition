import asyncio
import logging
from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from aiogram.enums.parse_mode import ParseMode

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"<b>Assalomu Aleykum {message.from_user.mention_html()}!</b>")


async def main() -> None:
    bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
