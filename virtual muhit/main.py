import asyncio
import logging
import sys

from aiogram import Bot,Dispatcher
from aiogram.enums import ParseMode

from config import TOKEN
from handlers.cmd_handlers import cmd_router
from handlers.reg_handlers import reg_router



async def main():
    bot=Bot(token=TOKEN,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
    dp=Dispatcher()
    dp.include_routers(cmd_router,reg_router)
    await dp.start_polling(bot)


if __name__=='main()':
    logging.basicConfig(level=logging.INFO,stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:


        print("Bot stop")




