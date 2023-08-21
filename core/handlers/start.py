from aiogram import types

from ..keyboards.default import get_default_keyboard

async def start_handler(message: types.Message, cb) -> None:
    await message.reply('Выберите пункт', reply_markup=get_default_keyboard(cb))
    # await add_user(message.from_user.id, message.from_user.full_name)