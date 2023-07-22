import time 
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from sqlite import db_start, add_user, add_record, get_records_month, get_categories

load_dotenv()

TOKEN = os.getenv('TOKEN')

sum_spent = 0

async def on_startup(_):
    await db_start()

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


### keyboards ###
def get_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(KeyboardButton('/amount'))
    kb.add(KeyboardButton('/analytics'))
    return kb

def get_category_keyboard(categories) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    # counter = 1
    # keyboard_row = ()

    for category in categories:
        # if (counter % 3 == 0):

        kb.add(KeyboardButton(category))

    return kb

def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

class ClientStates(StatesGroup):
    menu = State()
    amount = State()
    category = State()
    analytics = State()


### common handlers ###
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message) -> None:
    await ClientStates.menu.set()
    await message.reply('Выберите пункт', reply_markup=get_menu_keyboard())
    await add_user(message.from_user.id, message.from_user.full_name)


### menu handlers ###
@dp.message_handler(commands=['amount'], state=ClientStates.menu)
async def add_record_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ClientStates.amount)
    await message.reply('Введите сумму')

@dp.message_handler(state=ClientStates.amount)
async def amount_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ClientStates.category)
    async with state.proxy() as data:
        data['amount'] = int(message.text)

    categories = await get_categories()

    await message.reply('Выберите категорию', reply_markup=get_category_keyboard(categories))

@dp.message_handler(state=ClientStates.category)
async def category_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ClientStates.menu)

    async with state.proxy() as data:
        data['category'] = message.text

        await add_record(message.from_user.id, data['amount'], data['category'])

    await message.reply('Добавлено', reply_markup=get_menu_keyboard())


@dp.message_handler(commands=['analytics'], state=ClientStates.menu)
async def analytics_handler(message: types.Message, state: FSMContext) -> None: 
    total_month = await get_records_month(message.from_user.id)

    await message.reply(f'В этом месяце вы потратили: {total_month}', reply_markup=get_menu_keyboard())

@dp.message_handler(lambda message: not message.text.isdigit(), state=ClientStates.amount)
async def amount_handler_invalid(message: types.Message):
    return await message.reply("Сумма должна быть числом")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
