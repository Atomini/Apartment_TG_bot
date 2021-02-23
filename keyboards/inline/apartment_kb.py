from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

offers_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новобуд")],
        [InlineKeyboardButton(text="источник 2")],
        [InlineKeyboardButton(text="источник 3")],
        [InlineKeyboardButton(text="источник 4")]
    ]
)
