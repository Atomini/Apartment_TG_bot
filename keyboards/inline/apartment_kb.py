from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import bill_cb

offers_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новобуд", callback_data="novobud")],
        [InlineKeyboardButton(text="DomRia", callback_data="domria")],
        [InlineKeyboardButton(text="источник 3", callback_data="site3")],
        [InlineKeyboardButton(text="источник 4", callback_data="site4")],
        [InlineKeyboardButton(text="Главное меню", callback_data=bill_cb.new(action="main", level=0))]
    ]
)
