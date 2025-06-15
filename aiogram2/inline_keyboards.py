from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_keyboard = InlineKeyboardBuilder()
inline_keyboard.row(types.InlineKeyboardButton(text="Test Inline Button", callback_data="inline1"))
inline_keyboard.row(types.InlineKeyboardButton(text="Test Inline Button 2", callback_data="inline2"))