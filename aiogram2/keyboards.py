from aiogram import types

keyboard = [
    [types.KeyboardButton(text="Contact", request_contact=True), types.KeyboardButton(text="Location", request_location=True)]
]

keyboard_ = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
