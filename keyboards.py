#Кнопки с программами
import telebot
from telebot import types

# Клавиатура под строкой ввода для выбора функций бота
def greetkeyboard():
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_weather = types.KeyboardButton('Узнать погоду')
    keyboard_calc = types.KeyboardButton('Калькулятор')
    keyboard_magictext = types.KeyboardButton('Графика')

    start_keyboard.add(keyboard_weather)
    start_keyboard.add(keyboard_calc)
    start_keyboard.add(keyboard_magictext)
    return start_keyboard
