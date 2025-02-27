import asyncio
import aiohttp
from googletrans import Translator
from random import choices
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from Constant import question, rez, opisanie,t

router = Router()
translator = Translator()


class OrderWeather(StatesGroup):
    waiting_for_forecast = State()


async def opros(message):
    await message.answer(
        f"Выберите категорию:",
    )





@router.message(Command("Отправить_результат"))
async def weather_time(message: Message, command: CommandObject, state: FSMContext, requests=None):
    await message.answer(

        f" Чат связи с сотрудниками зоопарка https://web.telegram.org/a/#-1001762403226 ",

    )


@router.message(Command("Victirine"))
async def weather_time(message: Message, command: CommandObject, state: FSMContext):


    builder = ReplyKeyboardBuilder()
    for date_item in t:
        builder.add(types.KeyboardButton(text=date_item))
    builder.adjust(4)

    await message.answer(
        f"{question[0]}",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_data({'count': '', 'n': 1})
    await state.set_state(OrderWeather.waiting_for_forecast.state)


#
@router.message(OrderWeather.waiting_for_forecast)
async def weather_by_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['n'] < len(question):
        n = data['n']
    else:
        n = 1
    builder = ReplyKeyboardBuilder()
    for date_item in t:
        builder.add(types.KeyboardButton(text=date_item))
    builder.adjust(4)

    if message.text == 'Да':
        data['count'] = data['count'] + '1'
    if message.text == 'Нет':
        data['count'] = data['count'] + '0'
    await state.set_data({'count': data['count'], 'n': n + 1})

    if len(data['count']) != len(question):
        await state.set_state(OrderWeather.waiting_for_forecast.state)
        await message.answer(
            f"{question[n]}",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    else:
        try:
            await message.answer(

                f"Ваше тотемное животное :   {rez[data['count']]}  "

            )
            await message.answer(

                f" {opisanie}   ", end=" ",

            )

            await state.set_data({'count': '', 'n': 0})
        except:
            await message.answer(

                f"Что-то пошло не так, попробуйте снова ",

            )
