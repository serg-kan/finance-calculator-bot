from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_default_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text='Button 1', callback_data=cb_action.new('amount'))],
        # [InlineKeyboardButton(text='Button 2', callback_data=cb_action.new('analytics'))]
        [InlineKeyboardButton(text='Button 1', callback_data='text')],
        [InlineKeyboardButton(text='Button 2', callback_data='text')]
    ])

    return ikb