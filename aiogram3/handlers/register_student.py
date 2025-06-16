from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from states.register_student import RegisterStudent
from keyboards.phone_number import contact_keyboard
from keyboards.location import location_keyboard

router = Router()


@router.message(F.text == "Register a new student")
async def cmd_register_student(message: types.Message, state: FSMContext):
    await message.answer("Registratsiya boshlandi....")
    await state.set_state(RegisterStudent.first_name)
    await message.answer("Send first name:")


@router.message(RegisterStudent.first_name)
async def cmd_register_student2(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegisterStudent.last_name)
    await message.answer("Send last name:")


@router.message(RegisterStudent.last_name)
async def cmd_register_student3(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegisterStudent.grade)
    await message.answer("Send your grade:\nExample: 10A 23")


@router.message(RegisterStudent.grade)
async def cmd_register_student4(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await state.set_state(RegisterStudent.phone_number)
    await message.answer("Send a phone number:", reply_markup=contact_keyboard)


@router.message(RegisterStudent.phone_number, F.contact)
async def cmd_register_student5(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    await state.set_state(RegisterStudent.location)
    await message.answer("Send a location:", reply_markup=location_keyboard)


@router.message(RegisterStudent.location, F.location)
async def cmd_register_student6(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(location1=message.location.latitude, location2=message.location.longitude)
    await message.answer("Malumotlar qabul qilindi", reply_markup=types.ReplyKeyboardRemove())
    data = await state.get_data()
    await state.clear()

    first_name = data["first_name"]
    last_name = data.get("last_name", "Unknown")
    grade = data.get("grade", "Unknown")
    phone_number = data.get("phone_number", "Unknown")
    location1 = data.get("location1", "Unknown")  # latitude
    location2 = data.get("location2", "Unknown")  # longitude

    await bot.send_message(chat_id=message.from_user.id,
                           text=f"First name: {first_name}\nLast name: {last_name}\nGrade: {grade}\nPhone Number: {phone_number}")
    await bot.send_location(chat_id=message.from_user.id, latitude=location1, longitude=location2) # noqa
