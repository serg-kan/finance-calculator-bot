from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..utils.callback_action import ActionInfo

def get_default_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить запись', callback_data=ActionInfo(foo='amount').pack())],
        [InlineKeyboardButton(text='Аналитика', callback_data=ActionInfo(foo='analytics').pack())]
    ])

    return ikb