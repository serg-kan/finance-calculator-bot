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

from sqlite import db_start, create_profile, add_record, get_records_month

load_dotenv()

TOKEN = os.getenv('TOKEN')

async def on_startup(_):
    await db_start()

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

def get_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(KeyboardButton('/amount'))
    kb.add(KeyboardButton('/analytics'))
    return kb

def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

class ClientStates(StatesGroup):
    menu = State()
    amount = State()
    analytics = State()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message) -> None:
    await ClientStates.menu.set()
    await message.reply('Выберите пункт', reply_markup=get_menu_keyboard())
    await create_profile(message.from_user.id, message.from_user.full_name)

### Menu handlers
@dp.message_handler(commands=['amount'], state=ClientStates.menu)
async def amount_handler(message: types.Message, state:FSMContext) -> None:
    await state.set_state(ClientStates.amount)
    await message.reply('Введите сумму')

@dp.message_handler(commands=['analytics'], state=ClientStates.menu)
async def analytics_handler(message: types.Message, state:FSMContext) -> None: 
    total_month = await get_records_month(message.from_user.id)

    await message.reply(f'В этом месяце вы потратили: {total_month}', reply_markup=get_menu_keyboard())

@dp.message_handler(lambda message: not message.text.isdigit(), state=ClientStates.amount)
async def amount_handler_invalid(message: types.Message):
    return await message.reply("Сумма должна быть числом")

@dp.message_handler(state=ClientStates.amount)
async def amount_handler(message: types.Message, state:FSMContext) -> None:
    await state.set_state(ClientStates.menu)
    global sum_spent
    sum_spent += int(message.text)
    await message.reply(f'Вы ввели сумму: {int(message.text)}, общее: {sum_spent}', reply_markup=get_menu_keyboard())
    await add_record(int(message.text), message.from_user.id)


# @dp.message_handler(state='*', commands=['cancel'])
# async def cancel_handler(message: types.Message, state=FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state is None:
#         return
    
#     await state.finish()


# @dp.message_handler(lambda message: message.text.isdigit(), state=ClientStatedGroup.amount)
# async def amount_handler(message: types.Message, state: FSMContext):
#     global sum_spent

#     sum_spent += int(message.text)
#     await state.update_data(age=sum_spent)
#     await message.reply(f'Вы потратили: {sum_spent}')


# @dp.message_handler(Text(equals='Начать работу', ignore_case=True)):
# async def start_work_handler(message: types.Message):

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)