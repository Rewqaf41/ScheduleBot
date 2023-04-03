from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from utils.keybord import menu, choice
from main import bot, dp


@dp.message_handler(commands=['menu'], commands_prefix='!/')
async def show_menu(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    msg = await message.answer('Выберите действие:', reply_markup=menu)

    await dp.current_state().update_data(menu_message_id=msg.message_id)


@dp.message_handler()
async def schedule(message: Message, state: FSMContext):
    if message.text == '🗓Расписание':
        data = await state.get_data()
        menu_message_id = data.get('menu_message_id')
        if menu_message_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=menu_message_id)

        await message.answer(reply_markup=choice, text='Расписание по')

    elif message.text == '🏢Аудитории':
        await message.answer('А оно тебе надо?🤔')

    elif message.text == '👨‍🏫Преподавателю':
        search_type = 'препод'
        tg_id = message.from_user.id
        await message.answer(text='Введите фамилию преподавателя в формате: "ФИО"\n'
                                  '')
    elif message.text == '📚Группе':
        search_type = 'группа'
        tg_id = message.from_user.id
        # print(tg_id)
        await message.answer(text='Введите номер группы в формате: "Курс/Группа"\n'
                                  'Пример: 1/244')

    elif message.text == '⚙️Настройки':
        await message.answer('Лучше не лезь сюда, тут все-равно ничего нету!)')
