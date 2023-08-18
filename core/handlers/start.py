from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from ..keyboards.default import get_default_keyboard

async def start_handler(message: types.Message) -> None:
    await message.reply('Выберите пункт', reply_markup=get_defaul
    t_keyboard())
    # await add_user(message.from_user.id, message.from_user.full_name)