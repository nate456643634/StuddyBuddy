from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.start import start_router
from handlers.add_handler import add_router
from handlers.done_hanlder import done_router
from handlers.list_handler import list_router
from database import create_table, get_upcoming_deadlines, get_user_id


import os
import logging
import asyncio

load_dotenv()

bot = Bot(os.getenv("TOKEN_BOT"))
dp = Dispatcher()


async def check_deadlines(bot: Bot, chat_id: int):
    while True:
        tasks = await get_upcoming_deadlines()
        for task_id, task_name, deadline in tasks:
            await bot.send_message(chat_id,
                                   f"⏰ Reminder! Task '{task_name}' expires on {deadline}!"
                                   )
            asyncio.sleep(3600)



async def main():
    
    dp.include_router(list_router)
    dp.include_router(done_router)
    dp.include_router(add_router)
    dp.include_router(start_router)
    logging.basicConfig(level=logging.INFO)
    await create_table()
    await dp.start_polling(bot)
    asyncio.create_task(check_deadlines(bot, chat_id=get_user_id()))



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(" ")