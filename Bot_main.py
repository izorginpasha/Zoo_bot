import asyncio
from dotenv import load_dotenv
import os
import logging
import sys
from unittest.mock import call
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from zoo_handler import router
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section
)



# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
dp = Dispatcher()
dp.include_router(router)



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="Команды"),
            types.KeyboardButton(text="Описание бота"),
            types.KeyboardButton(text="Контакты"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,

    )

    await message.answer(f"Привет! Я бот московского зоопарка, с чего начнем?"
                         f"Можем поиграть /Victirine", reply_markup=keyboard
                         )


@dp.message(F.text.lower() == "команды")
async def commands(message: types.Message):
    response = as_list(
        as_marked_section(
            Bold("Команды:"),
            "/Victirine",

            marker="✅ ",
        ),
    )
    await message.answer(
        **response.as_kwargs()
    )


@dp.message(F.text.lower() == "контакты")
async def description(message: types.Message):

    await message.answer("Сайт зоопарка https://moscowzoo.ru/"
                         "Телеграмм канал https://web.telegram.org/a/#-1001762403226")


@dp.message(F.text.lower() == "описание бота")
async def description(message: types.Message):

    await message.answer("Этот бот помогает вам с выбором тотемного животного,"
                         " а также предоставляет справочную информацию по работе зоопарка")


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
