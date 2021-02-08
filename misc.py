import logging
from aiogram import Bot, Dispatcher
import os
import asyncio
from dotenv import load_dotenv  # для использования .env
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # импорт памяти для машини состояний

storage = MemoryStorage()  # обявляем память для машини состояния
load_dotenv()  # запускаем dotenv

TOKEN = os.getenv("TOKEN")
loop = asyncio.get_event_loop()  # TODO узнать что делает и как изменить время с 20 сек

bot = Bot(token=str(TOKEN), parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage=storage)

logging.basicConfig(level=logging.DEBUG)  # После окончания проекта изменить DEBUG -> INFO
