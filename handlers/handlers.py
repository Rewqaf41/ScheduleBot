from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.keybord import menu, choice
from main import bot, dp
from myconfig import admin_id
import datetime


class forParser(StatesGroup):
    amount = State()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(chat_id=admin_id, text=f'{message.from_user.first_name} {message.from_user.last_name}')
    await bot.send_message(chat_id=admin_id, text=message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id, text='Пропишите команду /menu')


@dp.message_handler(commands=['menu'], commands_prefix='!/')
async def show_menu(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    msg = await message.answer('Выберите действие:', reply_markup=menu)

    await dp.current_state().update_data(menu_message_id=msg.message_id)


@dp.message_handler()
async def schedule(message: Message, state: FSMContext):
    if datetime.date.today().weekday() == 6:
       await message.answer(text='Сегодня воскресенье, какие пары, иди поспи')
    else:
        if message.text == '🗓Расписание':
            data = await state.get_data()
            menu_message_id = data.get('menu_message_id')
            if menu_message_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=menu_message_id)

            await message.answer(reply_markup=choice, text='Расписание по')

    if message.text == '⚙️Настройки':
        await message.answer('Лучше не лезь сюда, тут все-равно ничего нету!)')


@dp.callback_query_handler(text='audit')
async def audit(call: CallbackQuery):
    await call.answer(text='А оно тебе надо?🤔', cache_time=60)
    await call.message.edit_reply_markup()

    await remove_schedule_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(text='group')
async def group(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await bot.send_message(chat_id=call.message.chat.id, text='Введите номер группы в формате: "Курс/Группа"\n'
                           'Пример: 1/244')
    await forParser.amount.set()

    await remove_schedule_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(text='prepod')
async def prepod(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await bot.send_message(chat_id=call.message.chat.id, text='Введите фамилию преподавателя в формате: "ФИО"\n')
    await forParser.amount.set()

    await remove_schedule_message(call.message.chat.id, call.message.message_id)


async def remove_schedule_message(chat_id, message_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass


@dp.message_handler(state=forParser.amount)
async def load_amount(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
        print(data['amount'])
    await state.finish()
