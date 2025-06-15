import asyncio
import logging
from aiogram import Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from keyboards import keyboard_

TOKEN = API_TOKEN

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"<b>Assalomu Aleykum, Xurmatli {message.from_user.mention_html()}</b>",
                         reply_markup=keyboard_)


@dp.message(F.contact)
async def cmd_receive_contact(message: types.Message):
    await message.answer("Contact qabul qilindi ✅")
    phone_number = message.contact.phone_number
    contact_name1 = message.contact.first_name
    contact_name2 = message.contact.last_name
    contact_user_name = f"{contact_name1} {contact_name2}"

    print(phone_number, contact_user_name)


@dp.message(F.location)
async def cmd_receive_location(message: types.Message):
    await message.answer("Location qabul qilindi ✅")
    location1 = message.location.latitude
    location2 = message.location.longitude

    print(location1, location2)


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
