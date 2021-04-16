from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import bill_cb

offers_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новобуд", callback_data="novobud")],
        [InlineKeyboardButton(text="DomRia", callback_data="domria")],
        [InlineKeyboardButton(text="OLX", callback_data="olx")],
        [InlineKeyboardButton(text="Flafy", callback_data="flafy")],
        [InlineKeyboardButton(text="Главное меню", callback_data=bill_cb.new(action="main", level=0))]
    ]
)
