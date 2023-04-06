import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InputFile

from main import bot, dp
from config import admin_id
from config import path_to_project
from utils.keybord import *
from schedule.parser import Parser


# Класс для машины состояний
class ForParser(StatesGroup):
    amount = State()


# Команда старт(для ознакомления с ботом)
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text='Пропишите команду /menu')


# Меню действий
@dp.message_handler(commands=['menu'], commands_prefix='!/')
async def show_menu(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    msg = await message.answer('Выберите действие:', reply_markup=menu)

    await dp.current_state().update_data(menu_message_id=msg.message_id)


# Хендлер для принятия комманд меню
@dp.message_handler()
async def schedule(message: Message, state: FSMContext):
    if datetime.date.today().weekday() == 6:
        await message.answer(text='Сегодня воскресенье, какие пары🤨, иди поспи😊')
    else:
        if message.text == '🗓Расписание':
            data = await state.get_data()
            menu_message_id = data.get('menu_message_id')
            #Удаление комманды '/menu'
            if menu_message_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=menu_message_id)
            #Возвращение инлайн меню с выбором
            await message.answer(reply_markup=choice, text='Расписание по')

    if message.text == '⚙️Настройки':
        await message.answer('Лучше не лезь сюда, тут все-равно ничего нету!)')


# Инлайн кнопка для аудитории(Кнопка прикол)
@dp.callback_query_handler(text='audit')    # нет аргумента сообщение))))
async def audit(call: CallbackQuery):
    await call.answer(text='А оно тебе надо?🤔', cache_time=60)
    await call.message.edit_reply_markup()

    await remove_schedule_message(call.message.chat.id, call.message.message_id)


# Инлайн кнопка, для группы
@dp.callback_query_handler(text='group')
async def group(call: CallbackQuery, state: FSMContext):
    search_type = 'группа'
    #Вызов машины состояний
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text='Расписание на сегодня, или другой день?', reply_markup=today_or_any_day)
    #Добавление переменной search_type в машину состояний
    await state.update_data(search_type=search_type)


# Инлайн кнопка, для преподавателя
@dp.callback_query_handler(text='prepod')
async def prepod(call: CallbackQuery, state: FSMContext):
    search_type = 'препод'
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    #Инлайн меню выбора дня
    await call.message.answer(text='Расписание на сегодня, или другой день?', reply_markup=today_or_any_day)
    #Добавление переменной search_type в машину состояний
    await state.update_data(search_type=search_type)


# Инлайн кнопка отвечающая за сегодняшний день
@dp.callback_query_handler(text='today')
async def today(call: CallbackQuery, state: FSMContext):
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    async with state.proxy() as data:
        if data.get('search_type') == 'группа':
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Введите номер группы в формате: "Курс/Группа"\n'
                                        'Пример: 1/244')
        elif data.get('search_type') == 'препод':
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Введите фамилию преподавателя в формате: "ФИО"\n')
    await ForParser.amount.set()


# Инлайн кнопка отвечающая за любой другой день
@dp.callback_query_handler(text='any_day')
async def any_day(call: CallbackQuery):

    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    #Вызов инлайн меню с выбором недели(1 или 2)
    await call.message.answer(text='Какая неделя?', reply_markup=weeks)


#Инлайн кнопки отвечающие за недели
@dp.callback_query_handler(text='first')
async def first(call: CallbackQuery, state: FSMContext):
    week = '1'
    await state.update_data(week=week)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text='Какой день?', reply_markup=weekdays)


@dp.callback_query_handler(text='second')
async def second(call: CallbackQuery, state: FSMContext):
    week = '2'
    await state.update_data(week=week)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text='Какой день?', reply_markup=weekdays)


# Инлайн кнопки отвечающие за дни недели
@dp.callback_query_handler(text='ПН')
async def monday(call: CallbackQuery, state: FSMContext):
    weekday = 'Понедельник'
    # добавление weekday в машину состояний
    await state.update_data(weekday=weekday)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    # вызываем функцию today, чтобы вернуть текст примера и войти в машину состояний
    await today(call, state)


@dp.callback_query_handler(text='ВТ')
async def tuesday(call: CallbackQuery, state: FSMContext):
    weekday = 'Вторник'
    # добавление weekday в машину состояний
    await state.update_data(weekday=weekday)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    # вызываем функцию today, чтобы вернуть текст примера и войти в машину состояний
    await today(call, state)


@dp.callback_query_handler(text='СР')
async def wednesday(call: CallbackQuery, state: FSMContext):
    weekday = 'Среда'
    # добавление weekday в машину состояний
    await state.update_data(weekday=weekday)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    # вызываем функцию today, чтобы вернуть текст примера и войти в машину состояний
    await today(call, state)


@dp.callback_query_handler(text='ЧТ')
async def thursday(call: CallbackQuery, state: FSMContext):
    weekday = 'Четверг'
    # добавление weekday в машину состояний
    await state.update_data(weekday=weekday)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    # вызываем функцию today, чтобы вернуть текст примера и войти в машину состояний
    await today(call, state)


@dp.callback_query_handler(text='ПТ')
async def friday(call: CallbackQuery, state: FSMContext):
    weekday = 'Пятница'
    # добавление weekday в машину состояний
    await state.update_data(weekday=weekday)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    # вызываем функцию today, чтобы вернуть текст примера и войти в машину состояний
    await today(call, state)


@dp.callback_query_handler(text='СБ')
async def saturday(call: CallbackQuery, state: FSMContext):
    weekday = 'Суббота'
    # добавление weekday в машину состояний
    await state.update_data(weekday=weekday)
    await remove_schedule_message(call.message.chat.id, call.message.message_id)
    # вызываем функцию today, чтобы вернуть текст примера и войти в машину состояний
    await today(call, state)


#Удаление сообщения бота
async def remove_schedule_message(chat_id, message_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass


#Машина состояний
@dp.message_handler(state=ForParser.amount)
async def load_amount(message: Message, state: FSMContext):
    async with state.proxy() as data:
        # берём переменные из машины состояний
        data['amount'] = message.text
        search_type = data.get('search_type')
        week = data.get('week')
        weekday = data.get('weekday')
    await state.finish()
    # Вычисляем, если переменные week и weekday возвращают None, вызываем парсер для сегодняшнего дня,
    # иначе парсер для любого дня
    if week is None and weekday is None:
        await bot.send_message(chat_id=message.from_user.id, text='Сейчас проверю...')
        schedule_today = Parser(search_type, data['amount'], message.from_user.id)
        if schedule_today.get_schedule_today():
            photo_today = InputFile(f'{path_to_project}/schedule/Data/res{message.from_user.id}.png')
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_today)
            msg_today = await message.answer('Выберите действие:', reply_markup=menu)
            await state.update_data(menu_message_id=msg_today.message_id)
            schedule_today.delete_cache()
            schedule_today.close_driver()
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Ничего не найдено('
                                                                      '\nПроверьте правильность введенных данных. Ну либо'
                                                                      ' сайт хима упал (:')
            await message.answer('Выберите действие:', reply_markup=menu)
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Сейчас проверю...')
        schedule_any_day = Parser(search_type, data['amount'], message.from_user.id)
        if schedule_any_day.get_schedule_on_any_day(week, weekday):
            photo_any_day = InputFile(f'{path_to_project}/schedule/Data/res{message.from_user.id}.png')
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_any_day)
            msg_any_day = await message.answer('Выберите действие:', reply_markup=menu)
            await state.update_data(menu_message_id=msg_any_day.message_id)
            schedule_any_day.delete_cache()
            schedule_any_day.close_driver()
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Ничего не найдено('
                                                                      '\nПроверьте правильность введенных данных. Ну либо'
                                                                      ' сайт хима упал (:')
            await message.answer('Выберите действие:', reply_markup=menu)
