import logging

from aiogram import Bot, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook

from config import TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode='HTML')
Bot.set_current(bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

webhook_path = f'/{TOKEN}'
webhook_url = f'https://6246-95-29-210-242.eu.ngrok.io{webhook_path}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8000


async def on_startup(dispatcher):
    await bot.set_webhook(webhook_url, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()

if __name__ == '__main__':
    from handlers import dp
    start_webhook(
        dispatcher=dp,
        webhook_path=webhook_path,
        skip_updates=False,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    # executor.start_polling(dp, skip_updates=False)
