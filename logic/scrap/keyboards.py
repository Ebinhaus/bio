from aiogram.types import ReplyKeyboardMarkup

def help_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Дай подсказку!")

def first_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add("2019", "2020", "2021", "2022", "2024")

def i_am_there():
    return ReplyKeyboardMarkup(resize_keyboard=True).add("Я тут!")