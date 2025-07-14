from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start", prefix='/@$'))
async def start(message: Message):
    await message.answer("""Hi! I’m your personal study assistant bot.
Here, you can create and manage learning tasks, set deadlines, mark tasks as complete — everything you need to stay organized and focused on your studies!

Use the following commands to get started:

    /add – Add a new task

    /done <id> – Mark a task as completed

    /list – View your current tasks and progress statistics

Start building better study habits today!""")
