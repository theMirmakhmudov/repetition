from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
from middleware import SubscriptionMiddleware
from keyboards import check

bot = Bot(token="7935939001:AAEAFZFDfnIlfiZ52B86hveDXowy0SdYV6k",
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Middleware ulash
dp.message.middleware(SubscriptionMiddleware())


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"<b>Assalomu Aleykum. Botimizga xush kelibsiz {message.from_user.mention_html()}\nBotdan foydalanish uchun quyidagi kanallarga obuna bo'ling:</b>",
        reply_markup=check)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Sizga qanday yordam bera olaman ?")


@dp.callback_query(F.data == "check")
async def process_check(call: types.CallbackQuery, bot: Bot):
    user_status = await bot.get_chat_member("-1002221838304", call.from_user.id)
    if user_status.status == "left":
        await call.answer("Kanalga xali obuna bo'lmagansiz !\nBirinchi kanalga obuna bo'ling", show_alert=True)
        await call.message.answer("<b>Botdan foydalanish uchun birinchi kanalga obuna bo'ling</b>", reply_markup=check)
        return

    await call.answer("<b>Botdan foydalanishingiz mumkin ✅</b>")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
