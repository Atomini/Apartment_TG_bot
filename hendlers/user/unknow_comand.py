from aiogram import types
from misc import dp


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def unknown_message(message: types.Message):
    await message.answer("Неизвесная команда. <b>Попробуйте "
                         "ввести другую команда</b>")
