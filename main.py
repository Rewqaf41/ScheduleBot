import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from myconfig import TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=False)