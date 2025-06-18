from aiogram import types

type_of_application = [
        "💼 Ish joyiga ariza",
        "🎓 Ta'lim muassasasiga ariza",
        "🏥 Tibbiy xizmat uchun ariza",
        "🏠 Uy-joy masalasi uchun ariza",
        "🔄 Boshqasi"
    ]

keyboard = [
    [types.KeyboardButton(text="💼 Ish joyiga ariza")],
    [types.KeyboardButton(text="🎓 Ta'lim muassasasiga ariza")],
    [types.KeyboardButton(text="🏥 Tibbiy xizmat uchun ariza")],
    [types.KeyboardButton(text="🏠 Uy-joy masalasi uchun ariza")],
    [types.KeyboardButton(text="🔄 Boshqasi")],
    [types.KeyboardButton(text="❌ Bekor qilish")]
]
type_of_application_keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="Ariza turini tanlang:")