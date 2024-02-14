
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


kb_request_contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)],
        [KeyboardButton(text="✉️ Emailni yuborish", request_contact=False)],
    ],
    resize_keyboard=True,
)
