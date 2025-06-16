from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("<b>Sizga qanday yordam bera olaman ?</b>")