from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Счет", callback_data="bill")],
        [InlineKeyboardButton(text="Квартиры", callback_data="apartment")]
    ]
)