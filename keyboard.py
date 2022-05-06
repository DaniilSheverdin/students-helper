from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('Расписание занятий', callback_data='gr_button')
inline_btn_2 = InlineKeyboardButton('Расписание экзаменов', callback_data='ex_button')
inline_btn_3 = InlineKeyboardButton('Адреса корпусов', callback_data='cs_button')
inline_btn_4 = InlineKeyboardButton('wolfram', callback_data='wf_button')
inline_btn_5 = InlineKeyboardButton('Мои ссылки', callback_data='lnk_button')

inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)

inline2_btn_1 = InlineKeyboardButton('Вывести', callback_data='select_button')
inline2_btn_2 = InlineKeyboardButton('Добавить', callback_data='add_button')
inline2_btn_3 = InlineKeyboardButton('Удалить', callback_data='del_button')

inline_kb2 = InlineKeyboardMarkup().add(inline2_btn_1, inline2_btn_2, inline2_btn_3)

button_hi = KeyboardButton('/menu')
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)

