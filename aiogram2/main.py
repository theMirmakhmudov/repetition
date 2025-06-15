import asyncio
import logging
from aiogram import Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from keyboards import keyboard_
from inline_keyboards import inline_keyboard

TOKEN = API_TOKEN

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"<b>Assalomu Aleykum, Xurmatli {message.from_user.mention_html()}</b>")

@dp.message(Command("button"))
async def cmd_button(message: types.Message):
    await message.answer("Keyboard Button", reply_markup=keyboard_)

@dp.message(Command("inline_button"))
async def cmd_inline_button(message: types.Message):
    await message.answer("Inline Keyboard Button", reply_markup=inline_keyboard.as_markup())

@dp.callback_query(F.data == "inline1")
async def cmd_inline_1(call: types.CallbackQuery):
    await call.message.answer("Salom men inline 1 man")


@dp.callback_query(F.data == "inline2")
async def cmd_inline_1(call: types.CallbackQuery):
    await call.message.answer("Salom men inline 2 man")

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
