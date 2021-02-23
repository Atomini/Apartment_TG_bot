from aiogram import types

from keyboards.inline import main_kb
from misc import dp


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text="Добро пожаловать в бот для поиска квартир в городе Полтава.\n"
                              "Виберите раздел для родолжения",
                         reply_markup=main_kb.main_keyboard)

