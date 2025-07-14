from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database import get_all_information

list_router = Router()

@list_router.message(Command('list'))
async def show_list(message: Message):
    try:
        task_info = await get_all_information()
        await message.answer(task_info)
    except Exception as e:
        await message.answer("Error")
        print(e)

