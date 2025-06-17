from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

start = [
    [
        InlineKeyboardButton(text="Сегодня", callback_data="today"),
        InlineKeyboardButton(text="Завтра", callback_data="tomorrow"),
        InlineKeyboardButton(text="Выбрать дату", callback_data="by_date"),
    ]
]

start_reply = [
    [
        KeyboardButton(text="Сегодня"),
        KeyboardButton(text="Завтра"),
        KeyboardButton(text="По дате"),
    ]
]

start_kb = InlineKeyboardMarkup(inline_keyboard=start)
start_reply_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=start_reply)
