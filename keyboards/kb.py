from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Photo')
b2 = KeyboardButton('/Audio')
b3 = KeyboardButton('/Voice')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb.add(b1).add(b2).add(b3)