import typing
from aiogram.types import CallbackQuery
from keyboards.inline import main_bill_kb, in_stock_change_kb, in_stock_kb
from keyboards.inline.bill_kb import confirm_cb
from keyboards.inline.callback_data import bill_cb
from misc import dp


@dp.callback_query_handler(text="bill")
async def bill(call: CallbackQuery):
    await call.answer(cache_time=20)
    await call.message.edit_text(text="Меню счет", reply_markup=main_bill_kb)


@dp.callback_query_handler(bill_cb.filter())
async def bill_menu(call: CallbackQuery, callback_data: typing.Dict[str, str]):
    await call.answer(cache_time=20)
    action = callback_data['action']
    level = callback_data['level']
    print(action, level)
    # TODO Добавить машину состояний для ячитивания данних
    if action == "stoke":
        await call.message.edit_text(text="В наличии", reply_markup=in_stock_change_kb)

    if action == "change" and level == "start":
        await call.message.edit_text(text="Что меняем", reply_markup=in_stock_kb)

    if action == "change" and level == "USD":
        await call.message.edit_text(text=f"меняем {level}, введите новуб сумму", reply_markup=confirm_cb)
