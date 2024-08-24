import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from os import getenv
from dotenv import load_dotenv

from keyboards import *
from dataworker import *

load_dotenv()
TOKEN=getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

dataworker = Dataworker("./data.xlsx")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет!\nЭтот бот поможет тебе понять <b>кто твои соседи!</b>\n"
        "Воспользуйся клавиатурой, выбрав этаж и комнату!\n\n"
        "<b>credits</b>: @engin3x",
        reply_markup=main_kb,
        parse_mode="html"
    )

@dp.message(F.text.lower() == "узнать соседей")
async def get_mates(message: Message):
    await message.answer(
        "Для того чтобы узнать соседей - выбери этаж!",
        reply_markup=create_floors()
        )
    
@dp.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    await bot.send_message(
        call.from_user.id,
        "Возвращение назад",
        reply_markup=main_kb
    )

@dp.callback_query(F.data.startswith("floor"))
async def floor(call: CallbackQuery):
    floor_number = int(call.data.split('-')[-1])
    floor_list = dataworker.get_floor_list(floor_number)

    await bot.send_message(
        call.from_user.id,
        "Выберите номер вашей комнаты!",
        reply_markup=create_rooms(floor_list)
    )

@dp.callback_query(F.data.startswith("room"))
async def room(call: CallbackQuery):
    room_number = int(call.data.split('-')[-1])
    room_list = dataworker.get_room_list(room_number)

    to_send = f"Проживающие в <b>комнате {room_number}</b>:\n\n"

    for person in room_list:
        to_send += f"{person}\n"
    
    await bot.send_message(
        call.from_user.id,
        to_send,
        parse_mode='html'
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try: asyncio.run(main())
    except BaseException: raise "Ended"