from aiogram.dispatcher.filters.state import State, StatesGroup


class StockDialog(StatesGroup):
    confirm = State()
    change = State()
    currency = State()