import typing

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database.table_function import add_new_user_to_bill, change_value_in_bill, get_from_bill
from keyboards.inline import main_bill_kb, in_stock_change_kb, in_stock_kb, goal_Kb, goal_change_kb
from keyboards.inline.bill_kb import confirm_cb
from keyboards.inline.callback_data import bill_cb
from misc import dp
from states import StockDialog
from aiogram import types


@dp.callback_query_handler(text="bill")
async def bill(call: CallbackQuery):
    add_new_user_to_bill(call.message.chat.id)
    await call.answer(cache_time=20)
    await call.message.edit_text(text="Меню счет", reply_markup=main_bill_kb)


@dp.callback_query_handler(bill_cb.filter())
async def bill_menu(call: CallbackQuery, callback_data: typing.Dict[str, str]):
    await call.answer(cache_time=20)
    action = callback_data['action']
    level = callback_data['level']
    global CURRENCY__
    global BILL_VAR__
# -------------------------------------bill block --------------------------------------------------
    if action == "stoke":

        USD = get_from_bill(call.message.chat.id,   'dollar')
        USD_E = get_from_bill(call.message.chat.id, 'dollar_elect')
        EUR = get_from_bill(call.message.chat.id,   'euro')
        EUR_E = get_from_bill(call.message.chat.id, 'euro_elect')
        UAH = get_from_bill(call.message.chat.id,   'grivna')
        UAH_E = get_from_bill(call.message.chat.id, 'grivna_elect')

        await call.message.edit_text(text="В наличии:\n"
                                          f"USD : {USD} \t  USD_E : {USD_E}\n"
                                          f"EUR : {EUR} \t  EUR_E : {EUR_E}\n"
                                          f"UAH : {UAH} \t  UAH_E : {UAH_E}\n"
                                          "В одной валюте: \n"
                                          "USD : 0000 \n"
                                          "EUR : 0000 \n"
                                          "UAH : 0000 ",
                                     reply_markup=in_stock_change_kb)

    if action == "change" and level == "start":
        await call.message.edit_text(text="Что меняем?", reply_markup=in_stock_kb)

    if action == "change" and level == "back":
        await call.message.edit_text(text="Меню счет", reply_markup=main_bill_kb)

    if action == "change" and level == "USD":
        CURRENCY__ = str(level)
        BILL_VAR__ = "dollar"
        await call.message.edit_text(text=f"Меняем {CURRENCY__}. Введите новую суму")
        await StockDialog.confirm.set()

    if action == "change" and level == "USD_elect":
        CURRENCY__ = str(level)
        BILL_VAR__ = "dollar_elect"
        await call.message.edit_text(text=f"Меняем {CURRENCY__}. Введите новую суму")
        await StockDialog.confirm.set()

    if action == "change" and level == "EUR":
        CURRENCY__ = str(level)
        BILL_VAR__ = "euro"
        await call.message.edit_text(text=f"Меняем {CURRENCY__}. Введите новую суму")
        await StockDialog.confirm.set()

    if action == "change" and level == "EUR_elect":
        CURRENCY__ = str(level)
        BILL_VAR__ = "euro_elect"
        await call.message.edit_text(text=f"Меняем {CURRENCY__}. Введите новую суму")
        await StockDialog.confirm.set()

    if action == "change" and level == "UAH":
        CURRENCY__ = str(level)
        BILL_VAR__ = "grivna"
        await call.message.edit_text(text=f"Меняем {CURRENCY__}. Введите новую суму")
        await StockDialog.confirm.set()

    if action == "change" and level == "UAH_elect":
        CURRENCY__ = str(level)
        BILL_VAR__ = "grivna_elect"
        await call.message.edit_text(text=f"Меняем {CURRENCY__}. Введите новую суму")
        await StockDialog.confirm.set()
# ----------------------------------        ---------------------------------------------------
    if action == "goal" and level == "0":
        GOAL = get_from_bill(call.message.chat.id, 'goal')
        INCOME = get_from_bill(call.message.chat.id, 'income')
        term = None
        full_UAH = None
        await call.message.edit_text(text=f"Цель составляет {GOAL} грн\n"
                                          f"Доход составляет {INCOME} грн\n"
                                          f"В наличии {full_UAH} грн\n"
                                          f"Приблизительное время до достижения цели{term} месяцев",
                                     reply_markup=goal_change_kb)

    if action == "goal" and level == "start":
        await call.message.edit_text(text="Что меняем?", reply_markup=goal_Kb)

    if action == "change" and level == "goal":
        CURRENCY__ = str(level)
        BILL_VAR__ = "goal"
        await call.message.edit_text(text=f"Меняем цель. Введите новую суму")
        await StockDialog.confirm.set()

    if action == "change" and level == "income":
        CURRENCY__ = str(level)
        BILL_VAR__ = "income"
        await call.message.edit_text(text=f"Меняем доход. Введите новую суму")
        await StockDialog.confirm.set()


@dp.message_handler(state=StockDialog.confirm)
async def change_money(message: types.Message, state: FSMContext):
    await state.update_data(summa=message.text)
    answer = message.text
    await StockDialog.next()
    await message.answer(text=f"Новая сума {answer}, {CURRENCY__}. Подтвердить?", reply_markup=confirm_cb)


@dp.callback_query_handler(state=StockDialog.change)
async def chan(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=20)
    if call.data == "bill:change:cancel":
        await state.finish()
        await call.message.answer(text="Изменение отменено", reply_markup=main_bill_kb)
    else:
        user_data = await state.get_data()
        await state.finish()
        change_value_in_bill(call.message.chat.id, BILL_VAR__, user_data['summa'])
        await call.message.answer(text=f"Новая сумма  {user_data['summa']} , {CURRENCY__}", reply_markup=main_bill_kb)

