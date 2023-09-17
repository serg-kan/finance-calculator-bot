from aiogram import types
from aiogram import Bot
from ..utils.sqlite import get_records_month

async def analytics_callback_handler(callback: types.CallbackQuery, bot: Bot):
    print('analytics callback handler', callback.from_user.id)
    total_month = await get_records_month(callback.from_user.id)

    await bot.send_message(callback.message.chat.id, f'В этом месяце вы потратили: {total_month}')
    await callback.answer('Analytics')