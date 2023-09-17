from aiogram.filters.callback_data import CallbackData

# cb_action = CallbackData('main', 'action')
class ActionInfo(CallbackData, prefix='my'):
  foo: str
