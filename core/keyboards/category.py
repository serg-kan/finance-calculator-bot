from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_category_keyboard(categories, cb) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)

    row = []
    count = 1
    for category in categories:
        row.append(InlineKeyboardButton(text=category, callback_data=cb.new(category)))
        if count % 3 == 0:
            ikb.add(*row)
            row = []
        count += 1
    
    return ikb