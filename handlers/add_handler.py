from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from database import add_tasks



class WaitingTaskInfo(StatesGroup):
    task_name = State()
    task_discription = State()
    task_datatime = State()

add_router = Router()


@add_router.message(Command("add"))
async def adding_tasks_name(message: Message, state: FSMContext):
    await state.set_state(WaitingTaskInfo.task_name)
    await message.answer("Enter the task name")



@add_router.message(WaitingTaskInfo.task_name)
async def add_task_discription(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.reply("Task name can't be empty!")
        return
    
    await state.update_data(task_name=message.text)
    await state.set_state(WaitingTaskInfo.task_discription)
    await message.answer("Now enter the discription for task: ")



@add_router.message(WaitingTaskInfo.task_discription)
async def add_datatime_task(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.reply("Discription can't be empty!")
        return
    
    await state.update_data(task_discription=message.text)
    await state.set_state(WaitingTaskInfo.task_datatime)
    await message.answer("Please enter the deadline in the format YYYY-MM-DD HH:MM:")



@add_router.message(WaitingTaskInfo.task_datatime)
async def add_deadline_task(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        datetime.strptime(message.text, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.reply("Invalid date format. Try again:")
        return
    
    data = await state.get_data()
    data["task_name"]
    data["task_discription"]

    await add_tasks(user_id=user_id,
                    task= data["task_name"],
                    discription=data["task_discription"],
                    deadline_str=message.text)
    
    await message.answer("Task is completed!")
    await state.clear()