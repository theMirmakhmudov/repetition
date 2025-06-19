from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text="Kanal nomi", url="t.me/all_hp")],
    [InlineKeyboardButton(text="Check", callback_data="check")],
])
