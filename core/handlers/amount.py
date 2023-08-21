from aiogram import types

from ..keyboards.category import get_category_keyboard
from ..utils.sqlite import get_categories

async def amount_callback_handler(callback: types.CallbackQuery, bot, cb_instance):

    # categories = await get_categories()
    # await bot.send_message(callback.from_user.id, 'Введите сумму', reply_markup=get_category_keyboard(categories, cb = cb_instance))
    await bot.send_message(callback.from_user.id, 'Введите сумму')
    await callback.answer()
