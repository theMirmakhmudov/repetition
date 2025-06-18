from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.application_form import ApplicationForm
from keyboards.type_of_application import type_of_application_keyboard, type_of_application
from keyboards.confirm_application import confirm
from config import GROUP_ID

router = Router()


@router.message(F.text == "📝 Ariza yuborish")
async def cmd_application(message: types.Message, state: FSMContext):
    await state.set_state(ApplicationForm.first_name)
    await message.answer(
        "📝 <b>Ariza berish jarayonini boshlaymiz!</b>\n\n"
        "👤 Iltimos, <b>ismingizni</b> kiriting:\n\n"
        "💡 <i>Masalan: Abdulla</i>",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ApplicationForm.first_name)
async def cmd_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text.title())
    await state.set_state(ApplicationForm.last_name)
    await message.answer(
        "👨‍👩‍👧‍👦 Endi <b>familiyangizni</b> kiriting:\n\n"
        "💡 <i>Masalan: Karimov</i>"
    )


@router.message(ApplicationForm.last_name)
async def cmd_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text.title())
    await state.set_state(ApplicationForm.age)
    await message.answer(
        "🎂 <b>Yoshingizni</b> kiriting:\n\n"
        "💡 <i>Faqat raqam kiriting (masalan: 25)</i>"
    )


@router.message(ApplicationForm.age)
async def cmd_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            "❌ <b>Noto'g'ri format!</b>\n"
            "Iltimos, yoshni faqat raqam ko'rinishida kiriting:"
        )
        return

    await state.update_data(age=message.text)
    await state.set_state(ApplicationForm.phone_number)
    await message.answer(
        "📱 <b>Telefon raqamingizni</b> kiriting:\n\n"
        "💡 <i>Masalan: +998901234567 yoki 901234567</i>"
    )


@router.message(ApplicationForm.phone_number)
async def cmd_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text

    if len(phone_number) < 9:
        await message.answer(
            "❌ <b>Telefon raqam juda qisqa!</b>\n"
            "Iltimos, to'liq telefon raqamini kiriting:"
        )
        return

    await state.update_data(phone_number=phone_number)
    await state.set_state(ApplicationForm.address)
    await message.answer(
        "🏠 <b>Manzilingizni</b> kiriting:\n\n"
        "💡 <i>Masalan: Toshkent shahar, Chilonzor tumani, Bunyodkor ko'chasi, 5-uy</i>"
    )


@router.message(ApplicationForm.address)
async def cmd_address(message: types.Message, state: FSMContext):
    if len(message.text) < 10:
        await message.answer(
            "❌ <b>Manzil juda qisqa!</b>\n"
            "Iltimos, to'liq manzilingizni kiriting:"
        )
        return

    await state.update_data(address=message.text)
    await state.set_state(ApplicationForm.application_type)
    await message.answer(
        "📋 <b>Ariza turini tanlang:</b>\n\n"
        "👇 Quyidagi variantlardan birini tanlang:",
        reply_markup=type_of_application_keyboard
    )


@router.message(ApplicationForm.application_type)
async def cmd_application_type(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer(
            "❌ <b>Ariza berish bekor qilindi!</b>",
            reply_markup=type_of_application_keyboard
        )
        return

    if not message.text in type_of_application:
        await message.answer(
            "❌ <b>Noto'g'ri tanlov!</b>\n"
            "Iltimos, ko'rsatilgan variantlardan birini tanlang:"
        )
        return

    await state.update_data(application_type=message.text)
    await state.set_state(ApplicationForm.application_description)
    await message.answer(
        "✍️ <b>Ariza matnini yozing:</b>\n\n"
        "📝 Batafsil yozing, bu sizning asosiy murojaatingiz.\n"
        "💡 Qancha ko'p ma'lumot bersangiz, shuncha tez javob olasiz!\n\n"
        "⏰ <i>Vaqtingizni band qilmaslik uchun, ariza matnini oldindan tayyorlab qo'ysangiz bo'ladi.</i>",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ApplicationForm.application_description)
async def cmd_application_description(message: types.Message, state: FSMContext, bot: Bot):
    if len(message.text) < 20:
        await message.answer(
            "❌ <b>Ariza matni juda qisqa!</b>\n"
            "Iltimos, kamida 20 ta belgi kiriting.\n"
            "Batafsil yozing, bu muhim:"
        )
        return

    await state.update_data(application_description=message.text)

    data = await state.get_data()
    await state.clear()

    global application_info
    application_info = (
        "📋 <b>SIZNING ARIZANGIZ:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Ism:</b> {data['first_name']}\n"
        f"👨‍👩‍👧‍👦 <b>Familiya:</b> {data['last_name']}\n"
        f"🎂 <b>Yosh:</b> {data['age']}\n"
        f"📱 <b>Telefon:</b> {data['phone_number']}\n"
        f"🏠 <b>Manzil:</b> {data['address']}\n"
        f"📋 <b>Ariza turi:</b> {data['application_type']}\n\n"
        f"✍️ <b>Ariza matni:</b>\n<i>{data['application_description']}</i>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "❓ <b>Ma'lumotlar to'g'rimi?</b>"
    )

    await message.answer(text=application_info, reply_markup=confirm.as_markup())


@router.callback_query(F.data == "confirm")
async def cmd_confirm(call: types.CallbackQuery, bot: Bot):
    await call.answer("Guruhga muvaffaqiyatli yuborildi ✅", show_alert=True)

    await bot.send_message(chat_id=GROUP_ID, text=application_info)