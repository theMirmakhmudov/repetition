from aiogram import Router, types
from aiogram.filters import Command
from keyboards.menu import menu_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_message = (
        f"🎉 <b>Assalomu alaykum, {message.from_user.full_name}!</b>\n\n"
        "📋 Men ariza qabul qiluvchi botman.\n"
        "🚀 Sizning arizangizni tez va oson tarzda "
        "tegishli bo'limga yetkazib beraman!\n\n"
        "💡 <b>Bot imkoniyatlari:</b>\n"
        "• Turli xil arizalar yuborish\n"
        "• Ma'lumotlarni xavfsiz saqlash\n"
        "• Tez javob olish\n"
        "• 24/7 xizmat\n\n"
        "🔽 <b>Quyidagi tugmalardan birini tanlang:</b>"
    )
    await message.answer(text=welcome_message, reply_markup=menu_keyboard)