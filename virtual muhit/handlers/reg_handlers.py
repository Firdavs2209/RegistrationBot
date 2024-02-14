from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,ReplyKeyboardRemove
import pdfkit
import tempfile
from config import DB_NAME
from keyboards.reg_keyboards import kb_request_contact
from states.reg_states import RegisterStates
from utils.database import Database
import tempfile
from aiogram import types
from pdf2image import convert_from_path


reg_router=Router()
db=Database(DB_NAME)


@reg_router.message(RegisterStates.regName)
async def register_name(message: Message, state: FSMContext):
    await message.answer("Iltimos, elektron pochta manzilingizni kiriting:")
    await state.update_data(regname=message.text)
    await RegisterStates.regEmail.set()

@reg_router.message(RegisterStates.regEmail)
async def register_email(message: Message, state: FSMContext):
    await message.answer("Iltimos, tug'ilgan yilingizni kiriting:")
    await state.update_data(regemail=message.text)
    await RegisterStates.regBirthYear.set()

@reg_router.message(RegisterStates.regBirthYear)
async def register_birth_year(message: Message, state: FSMContext):
    try:
        birth_year = int(message.text)
        # Here you can perform additional validation if needed

        reg_data = await state.get_data()
        reg_name = reg_data.get("regname")
        reg_email = reg_data.get("regemail")

        await message.answer(
            f"Hurmatli {reg_name}, siz tizimdan muvaffaqiyatli ro'yhatdan o'tdingiz!",
            reply_markup=ReplyKeyboardRemove()
        )
        db.update_user(message.from_user.id, reg_name, reg_email, birth_year)
        await state.finish()
    except ValueError:
        await message.answer("Iltimos, tug'ilgan yilni raqam formatida kiriting.")





@reg_router.message(F.photo & ~CommandStart())
async def handle_photo(message: types.Message, state: FSMContext):
    # Get the user ID
    user_id = message.from_user.id


    if state.get(user_id, 0) >= 3:
        await message.answer("Siz 3 marta rasm yuborganingiz uchun boshqa rasm yubora olmaysiz.")
        return


    state[user_id] = state.get(user_id, 0) + 1

    # Save the photo file
    temp_photo = tempfile.NamedTemporaryFile(suffix=".jpg")
    await message.photo[-1].download(temp_photo.name)

    pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf")
    pdfkit.from_file(temp_photo.name, pdf_file.name)


    await message.answer_document(types.InputFile(pdf_file.name))


    temp_photo.close()
    pdf_file.close()

    await message.answer("Rasm PDF ga o'girildi.")





@reg_router.message(F.text & ~CommandStart())
async def handle_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id


    user_data = await state.get_data()
    usage_count = user_data.get(user_id, 0)

    if usage_count >= 3:
        await message.answer("Siz 3 marta foydalandingiz, qaytadan so'rov qabul qila olmaysiz.")
        return

    if message.text.startswith(('https://multimediya.uz/e-kitob/')):

        temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf")


        pdfkit.from_url(message.text, temp_pdf.name)


        await message.answer_document(types.InputFile(temp_pdf.name))


        temp_pdf.close()
        usage_count += 1
        await state.update_data({user_id: usage_count})

        await message.answer("Sahifa pdfga o'girildi")
    else:
        await message.answer("Iltimos urlni yuboring.")
