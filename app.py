from aiogram import executor
from misc import dp
import hendlers

"""Точка входа. Запускать ТУТ!!!!"""

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=hendlers.admin.send_start_message,
                           on_shutdown=hendlers.admin.send_shutdown_message, skip_updates=True)
