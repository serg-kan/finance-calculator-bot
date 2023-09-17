from aiogram.utils.callback_data import CallbackData

class CategoryInfo(CallbackData, prefix='category'):
  category: str
