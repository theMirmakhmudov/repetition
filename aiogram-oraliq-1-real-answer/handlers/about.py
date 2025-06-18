from aiogram import Router, types, F

router = Router()


@router.message(F.text == "ℹ️ Ma'lumot")
async def cmd_about(message: types.Message):
    info_message = (
        "ℹ️ <b>BOT HAQIDA MA'LUMOT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 <b>Bu bot nima qiladi?</b>\n"
        "• Turli xil arizalar qabul qiladi\n"
        "• Ma'lumotlarni xavfsiz saqlaydi\n"
        "• Arizalarni tegishli bo'limga yetkazadi\n"
        "• 24/7 xizmat ko'rsatadi\n\n"
        "📋 <b>Ariza turlari:</b>\n"
        "• 💼 Ish joyiga ariza\n"
        "• 🎓 Ta'lim muassasasiga ariza\n"
        "• 🏥 Tibbiy xizmat uchun ariza\n"
        "• 🏠 Uy-joy masalasi uchun ariza\n"
        "• 🔄 Boshqa turlar\n\n"
        "⚡ <b>Afzalliklar:</b>\n"
        "• Tez va oson\n"
        "• Xavfsiz\n"
        "• Bepul\n"
        "• Har vaqt mavjud\n\n"
        "📞 <b>Yordam:</b> @admin_username"
    )
    await message.answer(text=info_message)
