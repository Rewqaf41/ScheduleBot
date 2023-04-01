from aiogram.types import Message

from utils.keybord import menu
from main import bot, dp
# from config import *


@dp.message_handler(commands=['menu'], commands_prefix='!/')
async def show_menu(message: Message):
    await message.answer(reply_markup=menu, text='👇Вот что есть👇')


@dp.message_handler()
async def schedule(message: Message):
    if message.text == '🗓Расписание':
        await message.answer(text=message.text)
    elif message.text == '⚙️Настройки':
        await message.answer(text=message.text)
