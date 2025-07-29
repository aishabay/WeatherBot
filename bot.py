import asyncio

import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import BOT_TOKEN
from keyboards import main_kb, inline_kb
from weather import get_weather

CHOICES = ["Камень", "Ножницы", "Бумага"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class CityForm(StatesGroup):
    waiting_for_city = State()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет. Выбери действие:", reply_markup=main_kb)


@dp.message(F.text == "Погода")
async def weather_button_clicked(message: Message, state: FSMContext):
    await message.answer("Название города:")
    await state.set_state(CityForm.waiting_for_city)


@dp.message(CityForm.waiting_for_city)
async def get_city_and_weather(message: Message, state: FSMContext):
    result = await get_weather(message.text)
    await message.answer(result)
    await state.clear()


@dp.message(F.text == "Камень-ножницы-бумага")
async def get_choice(message: Message, state: FSMContext):
    await message.reply("Выбери:",
                        reply_markup=inline_kb)


@dp.callback_query(F.data.in_(CHOICES))
async def get_result(callback: CallbackQuery):
    user_choice = callback.data
    bot_choice = random.choice(CHOICES)
    text = f"Ты выбрал: {user_choice}\nЯ выбрал: {bot_choice}\n\n"
    if user_choice == bot_choice:
        result = "Ничья!"
    elif (user_choice == "Камень" and bot_choice == "Ножницы") or \
         (user_choice == "Ножницы" and bot_choice == "Бумага") or \
         (user_choice == "Бумага" and bot_choice == "Камень"):
        result = "Вы выиграли!"
    else:
        result = "Вы проиграли!"

    await callback.message.edit_text(text + result)
    await callback.answer()


async def periodic_task():
    while True:
        try:
            await bot.send_message(
                chat_id=472243553,
                text="⏰ Reminder: This is your scheduled message!"
            )
        except Exception as e:
            print(f"Failed to send scheduled message: {e}")
        await asyncio.sleep(600)


async def on_startup():
    asyncio.create_task(periodic_task())


async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
