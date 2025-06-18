import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    ErrorEvent
)

# Bot tokenini o'rnating
BOT_TOKEN = "7935939001:AAEUDtEDkFgP_xCg6xXwJAliWgSb9aA0nvw"
GROUP_ID = "-1002221838304"  # Guruh ID sini o'rnating (- bilan boshlangan bo'lishi kerak)

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Router yaratish
main_router = Router()


# State'lar yaratish
class ArizaForm(StatesGroup):
    ism = State()
    familiya = State()
    yosh = State()
    telefon = State()
    manzil = State()
    ariza_turi = State()
    ariza_matn = State()
    tasdiqlash = State()


# Klaviatura builder funksiyalari
def get_main_menu() -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi"""
    kb = [
        [KeyboardButton(text="📝 Ariza yuborish")],
        [
            KeyboardButton(text="ℹ️ Ma'lumot"),
            KeyboardButton(text="📞 Aloqa")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Kerakli bo'limni tanlang..."
    )
    return keyboard


def get_ariza_turlari() -> ReplyKeyboardMarkup:
    """Ariza turlari klaviaturasi"""
    kb = [
        [KeyboardButton(text="💼 Ish joyiga ariza")],
        [KeyboardButton(text="🎓 Ta'lim muassasasiga ariza")],
        [KeyboardButton(text="🏥 Tibbiy xizmat uchun ariza")],
        [KeyboardButton(text="🏠 Uy-joy masalasi uchun ariza")],
        [KeyboardButton(text="🔄 Boshqasi")],
        [KeyboardButton(text="❌ Bekor qilish")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Ariza turini tanlang..."
    )
    return keyboard


def get_tasdiqlash() -> InlineKeyboardMarkup:
    """Tasdiqlash klaviaturasi"""
    kb = [
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash va yuborish",
                callback_data="confirm"
            )
        ],
        [
            InlineKeyboardButton(
                text="✏️ Tahrirlash",
                callback_data="edit"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="cancel"
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def get_edit_menu() -> InlineKeyboardMarkup:
    """Tahrirlash menyusi"""
    kb = [
        [
            InlineKeyboardButton(text="👤 Ism", callback_data="edit_ism"),
            InlineKeyboardButton(text="👨‍👩‍👧‍👦 Familiya", callback_data="edit_familiya")
        ],
        [
            InlineKeyboardButton(text="🎂 Yosh", callback_data="edit_yosh"),
            InlineKeyboardButton(text="📱 Telefon", callback_data="edit_telefon")
        ],
        [
            InlineKeyboardButton(text="🏠 Manzil", callback_data="edit_manzil"),
            InlineKeyboardButton(text="📋 Ariza turi", callback_data="edit_ariza_turi")
        ],
        [
            InlineKeyboardButton(text="✍️ Ariza matni", callback_data="edit_ariza_matn")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_confirm")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# /start komandasi
@main_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    """Bot boshlanishi"""
    await state.clear()  # Eski state'larni tozalash

    welcome_text = (
        f"🎉 <b>Assalomu alaykum, {message.from_user.full_name}!</b>\n\n"
        "📋 Men ariza qabul qiluvchi botman.\n"
        "🚀 Sizning arizangizni tez va oson tarzda "
        "tegishli bo'limga yetkazib beraman!\n\n"
        "💡 <b>Bot imkoniyatlari:</b>\n"
        "• Turli xil arizalar yuborish\n"
        "• Ma'lumotlarni xavfsiz saqlash\n"
        "• Tez javob olish\n"
        "• 24/7 xizmat\n\n"
        "🔽 <b>Quyidagi tugmalardan birini tanlang:</b>"
    )

    await message.answer(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu()
    )


# Ariza yuborish tugmasi
@main_router.message(F.text == "📝 Ariza yuborish")
async def ariza_start(message: Message, state: FSMContext) -> None:
    """Ariza berish jarayonini boshlash"""
    await state.set_state(ArizaForm.ism)

    await message.answer(
        "📝 <b>Ariza berish jarayonini boshlaymiz!</b>\n\n"
        "👤 Iltimos, <b>ismingizni</b> kiriting:\n\n"
        "💡 <i>Masalan: Abdulla</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )


# Ism kiritish
@main_router.message(StateFilter(ArizaForm.ism))
async def process_ism(message: Message, state: FSMContext) -> None:
    """Ism ma'lumotini qayta ishlash"""
    if len(message.text.strip()) < 2:
        await message.answer(
            "❌ <b>Ism juda qisqa!</b>\n"
            "Iltimos, to'liq ismingizni kiriting:",
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(ism=message.text.strip().title())
    await state.set_state(ArizaForm.familiya)

    await message.answer(
        "👨‍👩‍👧‍👦 Endi <b>familiyangizni</b> kiriting:\n\n"
        "💡 <i>Masalan: Karimov</i>",
        parse_mode=ParseMode.HTML
    )


# Familiya kiritish
@main_router.message(StateFilter(ArizaForm.familiya))
async def process_familiya(message: Message, state: FSMContext) -> None:
    """Familiya ma'lumotini qayta ishlash"""
    if len(message.text.strip()) < 2:
        await message.answer(
            "❌ <b>Familiya juda qisqa!</b>\n"
            "Iltimos, to'liq familiyangizni kiriting:",
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(familiya=message.text.strip().title())
    await state.set_state(ArizaForm.yosh)

    await message.answer(
        "🎂 <b>Yoshingizni</b> kiriting:\n\n"
        "💡 <i>Faqat raqam kiriting (masalan: 25)</i>",
        parse_mode=ParseMode.HTML
    )


# Yosh kiritish
@main_router.message(StateFilter(ArizaForm.yosh))
async def process_yosh(message: Message, state: FSMContext) -> None:
    """Yosh ma'lumotini qayta ishlash"""
    if not message.text.isdigit():
        await message.answer(
            "❌ <b>Noto'g'ri format!</b>\n"
            "Iltimos, yoshni faqat raqam ko'rinishida kiriting:",
            parse_mode=ParseMode.HTML
        )
        return

    yosh = int(message.text)
    if yosh < 14 or yosh > 100:
        await message.answer(
            "❌ <b>Yosh noto'g'ri!</b>\n"
            "Iltimos, 14 dan 100 gacha bo'lgan yoshni kiriting:",
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(yosh=message.text)
    await state.set_state(ArizaForm.telefon)

    await message.answer(
        "📱 <b>Telefon raqamingizni</b> kiriting:\n\n"
        "💡 <i>Masalan: +998901234567 yoki 901234567</i>",
        parse_mode=ParseMode.HTML
    )


# Telefon kiritish
@main_router.message(StateFilter(ArizaForm.telefon))
async def process_telefon(message: Message, state: FSMContext) -> None:
    """Telefon ma'lumotini qayta ishlash"""
    telefon = message.text.strip()

    # Telefon raqam validatsiyasi
    if len(telefon) < 9:
        await message.answer(
            "❌ <b>Telefon raqam juda qisqa!</b>\n"
            "Iltimos, to'liq telefon raqamini kiriting:",
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(telefon=telefon)
    await state.set_state(ArizaForm.manzil)

    await message.answer(
        "🏠 <b>Manzilingizni</b> kiriting:\n\n"
        "💡 <i>Masalan: Toshkent shahar, Chilonzor tumani, Bunyodkor ko'chasi, 5-uy</i>",
        parse_mode=ParseMode.HTML
    )


# Manzil kiritish
@main_router.message(StateFilter(ArizaForm.manzil))
async def process_manzil(message: Message, state: FSMContext) -> None:
    """Manzil ma'lumotini qayta ishlash"""
    if len(message.text.strip()) < 10:
        await message.answer(
            "❌ <b>Manzil juda qisqa!</b>\n"
            "Iltimos, to'liq manzilingizni kiriting:",
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(manzil=message.text.strip())
    await state.set_state(ArizaForm.ariza_turi)

    await message.answer(
        "📋 <b>Ariza turini tanlang:</b>\n\n"
        "👇 Quyidagi variantlardan birini tanlang:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_ariza_turlari()
    )


# Ariza turi tanlash
@main_router.message(StateFilter(ArizaForm.ariza_turi))
async def process_ariza_turi(message: Message, state: FSMContext) -> None:
    """Ariza turi tanlash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer(
            "❌ <b>Ariza berish bekor qilindi!</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu()
        )
        return

    ariza_turlari = [
        "💼 Ish joyiga ariza",
        "🎓 Ta'lim muassasasiga ariza",
        "🏥 Tibbiy xizmat uchun ariza",
        "🏠 Uy-joy masalasi uchun ariza",
        "🔄 Boshqasi"
    ]

    if message.text not in ariza_turlari:
        await message.answer(
            "❌ <b>Noto'g'ri tanlov!</b>\n"
            "Iltimos, ko'rsatilgan variantlardan birini tanlang:",
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(ariza_turi=message.text)
    await state.set_state(ArizaForm.ariza_matn)

    await message.answer(
        "✍️ <b>Ariza matnini yozing:</b>\n\n"
        "📝 Batafsil yozing, bu sizning asosiy murojaatingiz.\n"
        "💡 Qancha ko'p ma'lumot bersangiz, shuncha tez javob olasiz!\n\n"
        "⏰ <i>Vaqtingizni band qilmaslik uchun, ariza matnini oldindan tayyorlab qo'ysangiz bo'ladi.</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )


# Ariza matni kiritish
@main_router.message(StateFilter(ArizaForm.ariza_matn))
async def process_ariza_matn(message: Message, state: FSMContext) -> None:
    """Ariza matni qayta ishlash"""
    if len(message.text.strip()) < 20:
        await message.answer(
            "❌ <b>Ariza matni juda qisqa!</b>\n"
            "Iltimos, kamida 20 ta belgi kiriting.\n"
            "Batafsil yozing, bu muhim:",
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(ariza_matn=message.text.strip())
    await state.set_state(ArizaForm.tasdiqlash)

    # Ma'lumotlarni ko'rsatish
    data = await state.get_data()

    ariza_info = (
        "📋 <b>SIZNING ARIZANGIZ:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Ism:</b> {data['ism']}\n"
        f"👨‍👩‍👧‍👦 <b>Familiya:</b> {data['familiya']}\n"
        f"🎂 <b>Yosh:</b> {data['yosh']}\n"
        f"📱 <b>Telefon:</b> {data['telefon']}\n"
        f"🏠 <b>Manzil:</b> {data['manzil']}\n"
        f"📋 <b>Ariza turi:</b> {data['ariza_turi']}\n\n"
        f"✍️ <b>Ariza matni:</b>\n<i>{data['ariza_matn']}</i>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "❓ <b>Ma'lumotlar to'g'rimi?</b>"
    )

    await message.answer(
        ariza_info,
        parse_mode=ParseMode.HTML,
        reply_markup=get_tasdiqlash()
    )


# Tasdiqlash callback
@main_router.callback_query(F.data == "confirm", StateFilter(ArizaForm.tasdiqlash))
async def confirm_ariza(callback: CallbackQuery, state: FSMContext) -> None:
    """Arizani tasdiqlash va yuborish"""
    data = await state.get_data()

    # Guruhga yuborish uchun ma'lumotlarni tayyorlash
    user_info = (
        "🆕 <b>YANGI ARIZA KELDI!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>F.I.Sh:</b> {data['ism']} {data['familiya']}\n"
        f"🎂 <b>Yosh:</b> {data['yosh']} yosh\n"
        f"📱 <b>Telefon:</b> {data['telefon']}\n"
        f"🏠 <b>Manzil:</b> {data['manzil']}\n"
        f"📋 <b>Ariza turi:</b> {data['ariza_turi']}\n\n"
        f"✍️ <b>ARIZA MATNI:</b>\n"
        f"<blockquote>{data['ariza_matn']}</blockquote>\n\n"
        f"👤 <b>Telegram:</b> @{callback.from_user.username or 'Username yoq'}\n"
        f"🆔 <b>User ID:</b> <code>{callback.from_user.id}</code>\n"
        f"📅 <b>Sana:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    try:
        # Guruhga yuborish
        await callback.bot.send_message(
            chat_id=GROUP_ID,
            text=user_info,
            parse_mode=ParseMode.HTML
        )

        success_message = (
            "✅ <b>ARIZA MUVAFFAQIYATLI YUBORILDI!</b>\n\n"
            "🎯 Sizning arizangiz tegishli bo'limga yetkazildi.\n"
            "⏰ Tez orada sizga javob beramiz.\n\n"
            "📞 <b>Qo'shimcha savollar uchun:</b>\n"
            "• Telegram: @admin_username\n"
            "• Telefon: +998 90 123 45 67\n\n"
            "🙏 <b>Ishonch bildirganingiz uchun rahmat!</b>"
        )

        await callback.message.edit_text(
            success_message,
            parse_mode=ParseMode.HTML
        )

        await callback.message.answer(
            "🔄 <b>Boshqa ariza yuborish uchun tugmani bosing:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu()
        )

    except Exception as e:
        error_message = (
            "❌ <b>XATOLIK YUZ BERDI!</b>\n\n"
            "Iltimos, qaytadan urinib ko'ring yoki admin bilan bog'laning.\n\n"
            "📞 <b>Admin:</b> @admin_username"
        )

        await callback.message.edit_text(
            error_message,
            parse_mode=ParseMode.HTML
        )

        logger.error(f"Guruhga yuborishda xatolik: {e}")

    await state.clear()
    await callback.answer("✅ Ariza yuborildi!")


# Tahrirlash callback
@main_router.callback_query(F.data == "edit", StateFilter(ArizaForm.tasdiqlash))
async def edit_ariza(callback: CallbackQuery) -> None:
    """Arizani tahrirlash"""
    await callback.message.edit_text(
        "✏️ <b>Qaysi ma'lumotni tahrirlamoqchisiz?</b>\n\n"
        "👇 Quyidagi tugmalardan birini tanlang:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_edit_menu()
    )
    await callback.answer()


# Ma'lumot tugmasi
@main_router.message(F.text == "ℹ️ Ma'lumot")
async def info_handler(message: Message) -> None:
    """Bot haqida ma'lumot"""
    info_text = (
        "ℹ️ <b>BOT HAQIDA MA'LUMOT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 <b>Bu bot nima qiladi?</b>\n"
        "• Turli xil arizalar qabul qiladi\n"
        "• Ma'lumotlarni xavfsiz saqlaydi\n"
        "• Arizalarni tegishli bo'limga yetkazadi\n"
        "• 24/7 xizmat ko'rsatadi\n\n"
        "📋 <b>Ariza turlari:</b>\n"
        "• 💼 Ish joyiga ariza\n"
        "• 🎓 Ta'lim muassasasiga ariza\n"
        "• 🏥 Tibbiy xizmat uchun ariza\n"
        "• 🏠 Uy-joy masalasi uchun ariza\n"
        "• 🔄 Boshqa turlar\n\n"
        "⚡ <b>Afzalliklar:</b>\n"
        "• Tez va oson\n"
        "• Xavfsiz\n"
        "• Bepul\n"
        "• Har vaqt mavjud\n\n"
        "📞 <b>Yordam:</b> @admin_username"
    )

    await message.answer(
        info_text,
        parse_mode=ParseMode.HTML
    )


# Aloqa tugmasi
@main_router.message(F.text == "📞 Aloqa")
async def contact_handler(message: Message) -> None:
    """Aloqa ma'lumotlari"""
    contact_text = (
        "📞 <b>BIZ BILAN BOG'LANING</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "👨‍💼 <b>Administrator:</b>\n"
        "• Telegram: @admin_username\n"
        "• Telefon: +998 90 123 45 67\n\n"
        "📧 <b>Email:</b> admin@example.com\n"
        "🌐 <b>Veb-sayt:</b> www.example.com\n\n"
        "🕰 <b>ISH VAQTI:</b>\n"
        "• Dushanba - Juma: 09:00 - 18:00\n"
        "• Shanba: 09:00 - 13:00\n"
        "• Yakshanba: Dam olish kuni\n\n"
        "📍 <b>MANZIL:</b>\n"
        "Toshkent shahar, Chilonzor tumani\n"
        "Bunyodkor ko'chasi, 1-uy\n\n"
        "💬 <b>Savollaringiz bo'lsa, bemalol murojaat qiling!</b>"
    )

    await message.answer(
        contact_text,
        parse_mode=ParseMode.HTML
    )


# Bekor qilish callback
@main_router.callback_query(F.data == "cancel")
async def cancel_ariza(callback: CallbackQuery, state: FSMContext) -> None:
    """Arizani bekor qilish"""
    await state.clear()
    await callback.message.edit_text(
        "❌ <b>Ariza bekor qilindi!</b>\n\n"
        "🔄 Qaytadan boshlash uchun tugmani bosing:",
        parse_mode=ParseMode.HTML
    )
    await callback.message.answer(
        "👇 Boshqa xizmatlardan foydalaning:",
        reply_markup=get_main_menu()
    )
    await callback.answer("❌ Ariza bekor qilindi")


# State holatida bekor qilish
@main_router.message(F.text == "❌ Bekor qilish", StateFilter("*"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Har qanday holatda bekor qilish"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "❌ <b>Jarayon bekor qilindi!</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu()
    )


# Noma'lum xabarlar uchun handler
@main_router.message()
async def unknown_message(message: Message) -> None:
    """Noma'lum xabarlar"""
    await message.answer(
        "❓ <b>Kechirasiz, sizning xabaringiz tushunilmadi.</b>\n\n"
        "🔽 Quyidagi tugmalardan foydalaning:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu()
    )


# Xatoliklarni qaytarish
@main_router.error()
async def error_handler(event: ErrorEvent) -> None:
    """Xatoliklarni qaytarish"""
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)


async def main() -> None:
    """Bot ishga tushirish funksiyasi"""
    # Bot yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Dispatcher yaratish
    dp = Dispatcher(storage=MemoryStorage())

    # Router'ni qo'shish
    dp.include_router(main_router)

    # Bot ma'lumotlarini olish
    try:
        bot_info = await bot.get_me()
        logger.info(f"🚀 Bot ishga tushdi: @{bot_info.username}")
        logger.info(f"🤖 Bot nomi: {bot_info.full_name}")
        logger.info(f"🆔 Bot ID: {bot_info.id}")
    except Exception as e:
        logger.error(f"❌ Bot ma'lumotlarini olishda xatolik: {e}")
        return

    # Polling boshlanishi
    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    except Exception as e:
        logger.error(f"❌ Polling boshlanishida xatolik: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot to'xtatildi!")
    except Exception as e:
        logger.error(f"❌ Umumiy xatolik: {e}")