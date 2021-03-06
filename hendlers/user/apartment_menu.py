from aiogram.types import CallbackQuery

from database import get_from_novobud
from keyboards.inline import offers_kb
from misc import dp
from parser_bot.parser_bot.spiders.novobud import start_novobud


@dp.callback_query_handler(text="apartment")
async def apartment(call: CallbackQuery):
    await call.answer(cache_time=4)
    await call.message.edit_text(text="Выбирите источник:", reply_markup=offers_kb)


@dp.callback_query_handler(text="novobud")
async def novobud (call: CallbackQuery):
    await call.answer(cache_time=4)
    await call.message.edit_text(text="Собираем дание...\nПодождите несколько минут")
    start_novobud()
    data = get_from_novobud()
    for row in data:
        status = row[1]
        district = row[2]
        address = row[3]
        description = row[4]
        construction_end = row[5]
        link = row[6]
        image = row[7]
        price = row[8]
        map_d = row[9]
        map_w = row[10]
        await call.message.answer_photo(image)
        await call.message.answer_location(map_d, map_w)
        await call.message.answer(text=f"<b>Статус:</b> {status}\n"
                                       f"<b>Район:</b>  {district}\n"
                                       f"<b>Адресс:</b> {address}\n"
                                       f"<b>Окончание строительства:</b> {construction_end}\n"
                                       f"<b>Описание:</b> {description}\n"
                                       f"<b>Цена за грн/м2:</b>  {price}\n"
                                       f"<b>Цена за 40м2:</b> {int(price)*40}\n"
                                       f"<b>Ссылка:</b> {link}")
    await call.message.answer(text="<b>Подбор закончен</b>", reply_markup=offers_kb)



