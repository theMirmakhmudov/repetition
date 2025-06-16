from aiogram import types

keyboard = [
    [types.KeyboardButton(text="Register a new student")]
]

register_keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)