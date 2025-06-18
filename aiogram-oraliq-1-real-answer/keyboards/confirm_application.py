from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

confirm = InlineKeyboardBuilder()
confirm.row(types.InlineKeyboardButton(text="✅ Tasdiqlash va yuborish", callback_data="confirm"))