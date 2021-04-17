import os
from misc import bot

admin_id = os.getenv("admin_id")


async def send_start_message():
    await bot.send_message(chat_id=admin_id, text="Бот запущен /start")
