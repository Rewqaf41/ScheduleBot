from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🗓Расписание'),
        ],
        [
            KeyboardButton(text='⚙️Настройки')
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)

choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🏢Аудитории'),
            KeyboardButton(text='👨‍🏫Преподавателю'),
            KeyboardButton(text='📚Группе'),

        ],
    ],
    resize_keyboard=True
)