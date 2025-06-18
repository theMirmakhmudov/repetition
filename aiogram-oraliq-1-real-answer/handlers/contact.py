from aiogram import Router, types, F

router = Router()


@router.message(F.text == "📞 Aloqa")
async def cmd_contact(message: types.Message):
    contact_message = (
        "📞 <b>BIZ BILAN BOG'LANING</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "👨‍💼 <b>Administrator:</b>\n"
        "• Telegram: @admin_username\n"
        "• Telefon: +998 90 123 45 67\n\n"
        "📧 <b>Email:</b> admin@example.com\n"
        "🌐 <b>Veb-sayt:</b> www.example.com\n\n"
        "🕰 <b>ISH VAQTI:</b>\n"
        "• Dushanba - Juma: 09:00 - 18:00\n"
        "• Shanba: 09:00 - 13:00\n"
        "• Yakshanba: Dam olish kuni\n\n"
        "📍 <b>MANZIL:</b>\n"
        "Toshkent shahar, Chilonzor tumani\n"
        "Bunyodkor ko'chasi, 1-uy\n\n"
        "💬 <b>Savollaringiz bo'lsa, bemalol murojaat qiling!</b>"
    )
    await message.answer(text=contact_message)
