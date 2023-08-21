import time 
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from core.handlers.start import start_handler
from core.handlers.amount import amount_callback_handler
from core.handlers.analytics import analytics_callback_handler

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from core.utils.sqlite import db_start, add_user, add_record, get_records_month, get_categories

load_dotenv()

TOKEN = os.getenv('TOKEN')
PROXY_URL = os.getenv('PROXY_URL')

# 
# подумать, как совмещать инлайн клавиатуру и ввод суммы денег
# 

storage = MemoryStorage()
# bot = Bot(token=TOKEN, proxy=PROXY_URL)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

cb_action = CallbackData('main', 'action')
cb_category = CallbackData('main', 'category')

class ClientStates(StatesGroup):
    default = State()
    amount = State()
    category = State()
    analytics = State()

async def on_startup(_):
    await db_start()


### keyboards ###
def get_category_keyboard(categories) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)

    row = []
    count = 1
    for category in categories:
        row.append(InlineKeyboardButton(text=category, callback_data=cb_category.new(category)))
        if count % 3 == 0:
            ikb.add(*row)
            row = []
        count += 1
    
    return ikb


@dp.message_handler()
async def main_handler(message: types.Message):
    text = message.text

    if text == '/start':
         await start_handler(message, cb = cb_action)


### common handlers ###
@dp.callback_query_handler(cb_action.filter(action='amount'))
async def amount_handler(callback: types.CallbackQuery):
    await amount_callback_handler(callback, bot, cb_instance = cb_category)

@dp.callback_query_handler(cb_action.filter(action='analytics'))
async def analytics_handler(callback: types.CallbackQuery, callback_data: dict):
    await analytics_callback_handler(callback, callback_data)

@dp.callback_query_handler(cb_category.filter())
async def category_callback_handler(callback: types.CallbackQuery, callback_data: dict):
     await callback.answer(callback_data['category'])


# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup

# def get_menu_keyboard() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(resize_keyboard=True)

#     kb.add(KeyboardButton('/amount'))
#     kb.add(KeyboardButton('/analytics'))
#     return kb

# def get_category_keyboard(categories) -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(resize_keyboard=True)

#     # counter = 1
#     # keyboard_row = ()

#     for category in categories:
#         # if (counter % 3 == 0):

#         kb.add(KeyboardButton(category))

#     return kb

# def get_cancel() -> ReplyKeyboardMarkup:
#     return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))



# class ClientStates(StatesGroup):
#     menu = State()
#     amount = State()
#     category = State()
#     analytics = State()


# @dp.message_handler(commands=['amount'], state=ClientStates.menu)
# async def add_record_handler(message: types.Message, state: FSMContext) -> None:
#     await state.set_state(ClientStates.amount)
#     await message.reply('Введите сумму')

# @dp.message_handler(commands=['analytics'])
# async def analytics_handler(message: types.Message, state: FSMContext) -> None: 
#     await state.set_state(ClientStates.menu)

#     total_month = await get_records_month(message.from_user.id)

#     await message.reply(f'В этом месяце вы потратили: {total_month}', reply_markup=get_menu_keyboard())

# @dp.message_handler(state=ClientStates.amount)
# async def amount_handler(message: types.Message, state: FSMContext) -> None:
#     await state.set_state(ClientStates.category)
#     async with state.proxy() as data:
#         data['amount'] = int(message.text)

#     categories = await get_categories()

#     await message.reply('Выберите категорию', reply_markup=get_category_keyboard(categories))

# @dp.message_handler(state=ClientStates.category)
# async def category_handler(message: types.Message, state: FSMContext) -> None:
#     await state.set_state(ClientStates.menu)

#     async with state.proxy() as data:
#         data['category'] = message.text

#         await add_record(message.from_user.id, data['amount'], data['category'])

#     await message.reply('Добавлено', reply_markup=get_menu_keyboard())



# @dp.message_handler(lambda message: not message.text.isdigit(), state=ClientStates.amount)
# async def amount_handler_invalid(message: types.Message):
#     return await message.reply("Сумма должна быть числом")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)