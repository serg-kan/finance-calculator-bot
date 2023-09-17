from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import State, StatesGroup

from ..utils.callback_action import ActionInfo

from ..keyboards.category import get_category_keyboard
from ..utils.sqlite import get_categories


async def amount_callback_handler(callback: types.CallbackQuery, bot):
    print('amount callback handler', callback.from_user.id)
    # categories = await get_categories()
    # await bot.send_message(callback.from_user.id, 'Введите сумму', reply_markup=get_category_keyboard(categories, cb = cb_instance))
    await bot.send_message(callback.from_user.id, 'Введите сумму')
    await callback.answer()

def setup(dp: Dispatcher):
    print('amount setup')
    dp.callback_query.register(amount_callback_handler, ActionInfo.filter(F.foo=='amount'))


