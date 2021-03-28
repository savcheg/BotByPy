import math

import telebot
import pyowm
from pyowm.utils.config import get_default_config
from telebot import types

# TOKEN
bot = telebot.TeleBot('1791715945:AAHF0exJ-9gTdfhv5PXziJVugzQN3I1w0eI')

#Кнопки с программами
def greetkeyboard():
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_weather = types.KeyboardButton('☀Узнать погоду')
    keyboard_calc = types.KeyboardButton('📱Калькулятор')
    keyboard_magictext = types.KeyboardButton('🈹Символы')

    start_keyboard.add(keyboard_weather)
    start_keyboard.add(keyboard_calc)
    start_keyboard.add(keyboard_magictext)
    return start_keyboard

# Обработчик события приветствия
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBD5ZgYEMNgIdeeJb4_7IzqITscTWNOwAC0CsAAulVBRi_MsxcZV5XCh4E')
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup = greetkeyboard())
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBD5lgYEMPhQrPoYSg17wmU2cPEy1yowAC-isAAulVBRgEi75kjBko2h4E')

@bot.message_handler(content_types= ['text'])
def greeting(message):
    if message.text == '☀Узнать погоду':
        weather_set_place(message)
    elif message.text == '📱Калькулятор':
        getMeassage(message)
    elif message.text == '🈹Символы':
        magictext(message)

# Перевод слов в символы
alphabet =      {'А' : 0, 'Б' : 1, 'В' : 2, 'Г' : 3, 'Д' : 4, 'Е' : 5, 'Ж' : 6, 'З' : 7, 'И' : 8, 'К' : 9,
                 'Л' : 10, 'М' : 11, 'Н' : 12, 'О' : 13, 'П' : 14, 'Р' : 15, 'С' : 16, 'Т' : 17, 'У' : 18, 'Ф' : 19,
                 'Х' : 20, 'Ц' : 21, 'Ч' : 22, 'Ш' : 23, 'Щ' : 24, 'Ъ' : 25, 'Ы' : 26, 'Ь' : 27, 'Э' : 28, 'Ю' : 29,
                 'Я' : 30}

# Вводим слово
@bot.message_handler(commands=['magictext'])
def magictext(message):
    getWord = bot.send_message(message.chat.id, "Введите слово: ")
    bot.register_next_step_handler(getWord, outputWord)

# Выводим слово
def outputWord(message):
    onemsg = []
    word = message.text
    alphabet_sym = open('Alphabet3.txt')
    f = alphabet_sym.read()
    list = f.split(',\n')
    for i in range(len(word)):
         if word[i].isalpha():
             if word[i].upper() == 'Й':
                 index = alphabet.get('И')
             elif word[i].upper() == 'Ё':
                 index = alphabet.get('Е')
             else:
                index = alphabet.get(word[i].upper())
             onemsg.append(list[index])
         else:
            bot.send_message(message.chat.id, '\n'.join(onemsg), parse_mode='MarkdownV2')
            onemsg.clear()
    if word.lower() == 'пидр':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBD5xgYETzdnae2037gJTybN0Pa6KIEgAC2XUBAAFji0YMwe1-gje-P1geBA')
    else:
        bot.send_message(message.chat.id, '\n'.join(onemsg), parse_mode='MarkdownV2')

# Для погоды
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM('489f45987eb92460dc4955babb3bbeec', config_dict)

# Ввод города, о котором хотим узнать инфу о погоде
@bot.message_handler(commands=['weather'])
def weather_set_place(message):
    select_msg = bot.send_message(message.chat.id, "Выберите город: ")
    bot.register_next_step_handler(select_msg, weather_output)

# Вывод инфы о погоде
def weather_output(message):
    observation = owm.weather_manager().weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    answer = f"🏘 В городе {message.text}  {w.detailed_status}. \n"
    answer += "В данный момент температура около " + str(temp) + "°С." "\n"
    if temp < -20:
        answer += "🥶 На улице дубэо! Холодэо!"
    elif temp < -10:
        answer += "🥶 Думаю, лучше остаться дома!"
    elif temp < 0:
        answer += "😨 Пора менять резину!"
    elif temp < 10:
        answer += "😏 Уже не так холодно, можно гулять без куртки!"
    elif temp < 20:
        answer += "😏 Сейчас тепло. Скоро можно будет гулять в шортах!"
    elif temp > 20:
        answer += "🔥На улице жара!!! Го по пивасу!🔥"
    bot.send_message(message.chat.id, answer)

# Калькулятор
# Текущее значение калькулятора
value = ''
old_value = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row (  telebot.types.InlineKeyboardButton('C', callback_data='C'),
                telebot.types.InlineKeyboardButton('⬅', callback_data='<='),
                telebot.types.InlineKeyboardButton('➗', callback_data='/'))

keyboard.row (  telebot.types.InlineKeyboardButton('7️⃣', callback_data='7'),
                telebot.types.InlineKeyboardButton('8️⃣', callback_data='8'),
                telebot.types.InlineKeyboardButton('9️⃣', callback_data='9'),
                telebot.types.InlineKeyboardButton('✖', callback_data='*'))

keyboard.row (  telebot.types.InlineKeyboardButton('4️⃣', callback_data='4'),
                telebot.types.InlineKeyboardButton('5️⃣', callback_data='5'),
                telebot.types.InlineKeyboardButton('6️⃣', callback_data='6'),
                telebot.types.InlineKeyboardButton('➖', callback_data='-'))

keyboard.row (  telebot.types.InlineKeyboardButton('1️⃣', callback_data='1'),
                telebot.types.InlineKeyboardButton('2️⃣', callback_data='2'),
                telebot.types.InlineKeyboardButton('3️⃣', callback_data='3'),
                telebot.types.InlineKeyboardButton('➕', callback_data='+'))

keyboard.row (  telebot.types.InlineKeyboardButton('=', callback_data='='),
                telebot.types.InlineKeyboardButton('0️⃣', callback_data='0'),
                telebot.types.InlineKeyboardButton(',', callback_data=','))


# Обработчик события вызова калькулятора
@bot.message_handler(commands=['calculator'])
def getMeassage(message):
    global value
    if value == '':
       bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)

# Программа калькулятора
@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        try:
            value = str( eval(value) )
        except:
            value = 'Ошибка!'
    else:
        value += data

    if (value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=keyboard)
            old_value = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup=keyboard)
            old_value = value

    if value == 'Ошибка!':
        value = ''


# Запуск бота
#bot.polling(none_stop=True, interval=0)
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            telebot.logger.error(ex)