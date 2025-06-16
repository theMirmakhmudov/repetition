from aiogram import types

keyboard = [
    [types.KeyboardButton(text="Share Location", request_location=True)]
]

location_keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="Location yuboring please")