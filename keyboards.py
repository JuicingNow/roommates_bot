from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Узнать соседей")]
    ], resize_keyboard=True
)

def create_floors():
    items = [str(el) for el in range(1,6)]
    builder = InlineKeyboardBuilder()
    [builder.button(text=item, callback_data=f"floor-{item}") for item in items]
    builder.button(text="Назад", callback_data="back")
    builder.adjust(3,2,1)

    return builder.as_markup()

def create_rooms(floor_list):
    items = floor_list
    builder = InlineKeyboardBuilder()
    [builder.button(text=item, callback_data=f"room-{item}") for item in items]
    builder.button(text="Назад", callback_data="back")

    step = (len(items) - (len(items)%5)) // 5
    rest = len(items)%5
    
    if rest != 0: builder.adjust(*[5] * step, rest, 1)
    else: builder.adjust(*[5] * step, 1)

    return builder.as_markup()