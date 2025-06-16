from aiogram import types

keyboard = [
    [types.KeyboardButton(text="Share Contact", request_contact=True)]
]

contact_keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="Contactingizni yuboring: ")