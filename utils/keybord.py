from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🗓Расписание'),
        ],
        [
            KeyboardButton(text='⚙️Настройки')
        ],
    ],
    resize_keyboard=True
)

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            KeyboardButton(text='👨‍🏫Преподавателю', callback_data="prepod"),
            KeyboardButton(text='📚Группе', callback_data="group"),
        ],
        [
            KeyboardButton(text='🏢Аудитории', callback_data="audit"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)