from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🗓Расписание'),
        ],
    ],
    resize_keyboard=True
)

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👨‍🏫Преподавателю', callback_data="prepod"),
            InlineKeyboardButton(text='📚Группе', callback_data="group"),
        ],
        [
            InlineKeyboardButton(text='🏢Аудитории', callback_data="audit"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)

today_or_any_day = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='На сегодня', callback_data="today"),
            InlineKeyboardButton(text='На другой день', callback_data="any_day"),
        ],
        [
            InlineKeyboardButton(text='На все недели', callback_data="full_schedule")
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)

weeks = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data="first"),
            InlineKeyboardButton(text='2', callback_data="second"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)

weekdays = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='ПН', callback_data="ПН"),
            InlineKeyboardButton(text='ВТ', callback_data="ВТ"),
            InlineKeyboardButton(text='СР', callback_data="СР"),
        ],
        [
            InlineKeyboardButton(text='ЧТ', callback_data="ЧТ"),
            InlineKeyboardButton(text='ПТ', callback_data="ПТ"),
            InlineKeyboardButton(text='СБ', callback_data="СБ"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)