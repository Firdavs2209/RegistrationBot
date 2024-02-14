from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from keyboards.reg_keyboards import kb_request_contact
from utils.database import Database
from config import DB_NAME

db = Database(DB_NAME)

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    user = db.get_user(message.from_user.id)
    if not user:
        await message.answer(text="Iltimos, tug'ilgan yilingizni va email manzilingizni kiriting:",
                             reply_markup=kb_register)
    elif not user[6]:
        await message.answer(text="Iltimos, tug'ilgan yilingizni va email manzilingizni kiriting:",
                             reply_markup=kb_register)


@cmd_router.message(F.text & ~CommandStart())
async def handle_text(message: Message, state: dict):
    birth_year, email = message.text.split()


    db.update_user(message.from_user.id, birth_year, email)

    await message.answer("Rahmat! Ma'lumotlar saqlandi.")
