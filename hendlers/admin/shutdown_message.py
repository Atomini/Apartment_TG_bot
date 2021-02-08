import os
from misc import bot
import logging

admin_id = os.getenv("admin_id")


async def send_shutdown_message(dp):
    logging.warning('Shutting down..')
    await bot.send_message(chat_id=admin_id, text="Бот остановлен")
    await dp.storage.close()
    await dp.storage.wait_closed()
