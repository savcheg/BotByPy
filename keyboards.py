#Кнопки с программами
import telebot
from telebot import types

# Клавиатура под строкой ввода для выбора функций бота
def greetkeyboard():
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_weather = types.KeyboardButton('☀Узнать погоду')
    keyboard_calc = types.KeyboardButton('📱Калькулятор')
    keyboard_magictext = types.KeyboardButton('🈹Символы')
    keyboard_anekdot = types.KeyboardButton('🤣Анекдот')

    start_keyboard.add(keyboard_weather)
    start_keyboard.add(keyboard_calc)
    start_keyboard.add(keyboard_magictext)
    start_keyboard.add(keyboard_anekdot)
    return start_keyboard

# Клавиатура для калькулятора
def calckeyboard():
    calckeyboard = telebot.types.InlineKeyboardMarkup()
    calckeyboard.row (  telebot.types.InlineKeyboardButton('C', callback_data='C'),
                    telebot.types.InlineKeyboardButton('⬅', callback_data='<='),
                    telebot.types.InlineKeyboardButton('➗', callback_data='/'))

    calckeyboard.row (  telebot.types.InlineKeyboardButton('7️⃣', callback_data='7'),
                    telebot.types.InlineKeyboardButton('8️⃣', callback_data='8'),
                    telebot.types.InlineKeyboardButton('9️⃣', callback_data='9'),
                    telebot.types.InlineKeyboardButton('✖', callback_data='*'))

    calckeyboard.row (  telebot.types.InlineKeyboardButton('4️⃣', callback_data='4'),
                    telebot.types.InlineKeyboardButton('5️⃣', callback_data='5'),
                    telebot.types.InlineKeyboardButton('6️⃣', callback_data='6'),
                    telebot.types.InlineKeyboardButton('➖', callback_data='-'))

    calckeyboard.row (  telebot.types.InlineKeyboardButton('1️⃣', callback_data='1'),
                    telebot.types.InlineKeyboardButton('2️⃣', callback_data='2'),
                    telebot.types.InlineKeyboardButton('3️⃣', callback_data='3'),
                    telebot.types.InlineKeyboardButton('➕', callback_data='+'))

    calckeyboard.row (  telebot.types.InlineKeyboardButton('=', callback_data='='),
                    telebot.types.InlineKeyboardButton('0️⃣', callback_data='0'),
                    telebot.types.InlineKeyboardButton(',', callback_data=','))
    return calckeyboard