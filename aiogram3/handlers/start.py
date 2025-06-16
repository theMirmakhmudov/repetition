from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.start import register_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"<b>Assalomu Aleykum, Xurmatli {message.from_user.mention_html()}</b>",
                         reply_markup=register_keyboard)

