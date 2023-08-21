from aiogram import types

async def analytics_callback_handler(callback: types.CallbackQuery, callback_data: dict):
        await callback.answer('Analytics')