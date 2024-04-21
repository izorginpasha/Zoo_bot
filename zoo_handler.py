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
from Constant import question, rez

router = Router()
translator = Translator()


class OrderWeather(StatesGroup):
    waiting_for_forecast = State()
    waiting = State()


async def opros(message):
    await message.answer(
        f"Выберите категорию:",
    )


@router.message(Command("Victirine"))
async def weather_time(message: Message, command: CommandObject, state: FSMContext):
    data = ['Да', 'Нет']

    # await state.set_data({'count': command.args, 'data_recip': data})
    builder = ReplyKeyboardBuilder()
    for date_item in data:
        builder.add(types.KeyboardButton(text=date_item))
    builder.adjust(4)

    await message.answer(
        f"Выберите категорию:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_data({'count': ''})
    await state.set_state(OrderWeather.waiting_for_forecast.state)


@router.message(OrderWeather.waiting_for_forecast)
async def weather_by_date(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # async with aiohttp.ClientSession() as session:
    #     list = await list_recipes(session, message.text, data['count'])
    # await state.set_data({'list': list})

    if message.text == 'Да':
        data['count'] = data['count'] + '1'
    else:
        data['count'] = data['count'] + '0'
    await state.set_data({'count': data['count']})


    await message.answer(

        f"Как вам такие варианты: {data['count']}  ",


    )
    if len(data['count']) != len(question):
        await state.set_state(OrderWeather.waiting_for_forecast.state)
    else:
        await message.answer(

            f"Ваше тотемное животное волк: {rez[data['count']]}  ",

        )
