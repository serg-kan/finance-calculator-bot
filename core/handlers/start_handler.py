from aiogram import types, Dispatcher
from aiogram.filters import Command


from ..utils.sqlite import add_user


from ..keyboards.default import get_default_keyboard

async def start_handler(message: types.Message) -> None:
    await message.reply('Выберите пункт', reply_markup=get_default_keyboard())
    await add_user(message.from_user.id, message.from_user.full_name)

def setup(dp: Dispatcher):
    print('start_handler setup')
    dp.message.register(start_handler, Command(commands='start'))