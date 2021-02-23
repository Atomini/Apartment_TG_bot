from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import bill_cb


main_bill_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Курс", callback_data=bill_cb.new(action="course", level=0))],
        [InlineKeyboardButton(text="В наличии", callback_data=bill_cb.new(action="stoke", level=0))],
        [InlineKeyboardButton(text="Цель", callback_data=bill_cb.new(action="goal", level=0))],
        [InlineKeyboardButton(text="Главное меню", callback_data=bill_cb.new(action="main", level=0))]
    ]
)

in_stock_change_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить", callback_data=bill_cb.new(action="change", level="start"))]
    ]
)

in_stock_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="USD", callback_data=bill_cb.new(action="change", level="USD")),
         InlineKeyboardButton(text="USD_elect", callback_data=bill_cb.new(action="change", level="USD_elect"))],
        [InlineKeyboardButton(text="EUR", callback_data=bill_cb.new(action="change", level="EUR")),
         InlineKeyboardButton(text="EUR_elect", callback_data=bill_cb.new(action="change", level="EUR_elect"))],
        [InlineKeyboardButton(text="UAH", callback_data=bill_cb.new(action="change", level="UAH")),
         InlineKeyboardButton(text="UAH_elect", callback_data=bill_cb.new(action="change", level="UAH_elect"))]
    ]
)

confirm_cb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data=bill_cb.new(action="change", level="confirm"))]
    ]
)

back_cb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=bill_cb.new(action="change", level="back"))]
    ]
)