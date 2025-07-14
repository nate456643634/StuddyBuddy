from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from database import mark_task_as_done, get_user_task
from aiogram.exceptions import TelegramAPIError
import logging
done_router = Router()


@done_router.message(Command("done"))
async def done(message: Message, command: CommandObject):
   if not command.args:
      await message.answer("Use the index task to convert its index to start at zero")
      return
   try:
      task_id = int(command.args)
   except ValueError:
      await message.answer("The task number must be an integer.")
      return
    
   task = await get_user_task(task_id=task_id, user_id=message.from_user.id)

   if not task:
      await message.answer(f"Task with number {task_id} does not exist or does not belong to you")
      return
   try:
      await mark_task_as_done(task['id'])
      await message.answer(f"Task <b>«{task['name']}»</b> has been marked as completed!")
   except TelegramAPIError as e:
      await message.answer("Failed to update task. Try again later.")
      logging.error(f"Error marking task done: {e}")