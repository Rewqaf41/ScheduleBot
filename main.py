import logging

from aiogram import Bot, Dispatcher, executor
from myconfig import TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


if __name__ == '__main__':
    from handlers.handlers import dp
    executor.start_polling(dp, skip_updates=False)