import os

from aiogram.types import message

from misc import bot


admin_id = os.getenv("admin_id")


async def send_start_message(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен /start")
