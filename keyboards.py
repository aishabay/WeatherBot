from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Погода")],
        [KeyboardButton(text="Камень-ножницы-бумага")]
    ],
    resize_keyboard=True
)


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Камень",
                              callback_data="Камень")],
        [InlineKeyboardButton(text="Ножницы",
                              callback_data="Ножницы")],
        [InlineKeyboardButton(text="Бумага",
                              callback_data="Бумага")]
    ]
)
