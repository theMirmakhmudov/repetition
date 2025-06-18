from aiogram import types

keyboard = [
    [types.KeyboardButton(text="📝 Ariza yuborish")],
    [types.KeyboardButton(text="ℹ️ Ma'lumot"), types.KeyboardButton(text="📞 Aloqa")]
]
menu_keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)