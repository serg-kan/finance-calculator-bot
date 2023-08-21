from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_default_keyboard(cb) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Button 1', callback_data=cb.new('amount'))],
        [InlineKeyboardButton(text='Button 2', callback_data=cb.new('analytics'))]
    ])

    return ikb