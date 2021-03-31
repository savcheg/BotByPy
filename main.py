import pyowm
from pyowm.utils.config import get_default_config
import keyboards as kb
import telebot, bs4, requests


# TOKEN
bot = telebot.TeleBot('1791715945:AAHF0exJ-9gTdfhv5PXziJVugzQN3I1w0eI')


# Обработчик события приветствия
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBD5ZgYEMNgIdeeJb4_7IzqITscTWNOwAC0CsAAulVBRi_MsxcZV5XCh4E')
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup = kb.greetkeyboard())
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBD5lgYEMPhQrPoYSg17wmU2cPEy1yowAC-isAAulVBRgEi75kjBko2h4E')


@bot.message_handler(content_types= ['text'])
def greeting(message):
    if message.text == '☀Узнать погоду':
        setlocation(message)
    elif message.text == '📱Калькулятор':
        getMeassage(message)
    elif message.text == '🈹Символы':
        magictext(message)
    elif message.text == '🤣Анекдот':
        bot.send_message(message.chat.id, 'Осторожно❗ Кринж ❗❗❗')
        bot.send_message(message.from_user.id, getanekdot(), kb.greetkeyboard())


def getanekdot():
    z=''
    s=requests.get('http://anekdotme.ru/random')
    b=bs4.BeautifulSoup(s.text, "html.parser")
    p=b.select('.anekdot_text')
    for x in p:
        s=(x.getText().strip())
        z=z+s+'\n\n'
    return s

# Погода
url = 'http://api.openweathermap.org/data/2.5/weather'
api_weather = '489f45987eb92460dc4955babb3bbeec'
api_telegram = '1791715945:AAHF0exJ-9gTdfhv5PXziJVugzQN3I1w0eI'
@bot.message_handler(commands=['weather'])
def setlocation(message):
    location = bot.send_message(message.chat.id, 'Выберете город:')
    bot.register_next_step_handler(location, outWeatherInfo)

def outWeatherInfo(message):
    city_name = message.text

    try:
        params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'ru'}
        result = requests.get(url, params=params)
        weather = result.json()

        if weather["main"]['temp'] < -20:
            status = "🥶На улице дубэо! Холодэо!"
        elif weather["main"]['temp'] < -10:
            status = "🥶Думаю, лучше остаться дома!"
        elif weather["main"]['temp'] < 0:
            status = "😨Пора менять резину!"
        elif weather["main"]['temp'] < 10:
            status = "😏Сейчас холодновато!"
        elif weather["main"]['temp'] < 20:
            status = "🔥Сейчас тепло!"
        elif weather["main"]['temp'] > 25:
            status = "🔥Сейчас жарко!"
        else:
            status = "🔥Сейчас отличная температура!"

        bot.send_message(message.chat.id, "🌡В городе " + str(weather["name"]) + " температура " + str(
            float(weather["main"]['temp'])) + " °C\n" +
                         "📈Максимальная температура " + str(float(weather['main']['temp_max'])) + " °C\n" +
                         "📉Минимальная температура " + str(float(weather['main']['temp_min'])) + " °C\n" +
                         "💨Скорость ветра " + str(float(weather['wind']['speed'])) + " м/с\n" +
                         "🅿️Давление " + str(float(weather['main']['pressure'])) + " мбар\n" +
                         "💦Влажность " + str(int(weather['main']['humidity'])) + " %\n" +
                         "👀Видимость " + str(weather['visibility']) + "\n" +
                         "📜Описание: " + str(weather['weather'][0]["description"]) + "\n\n" + status, kb.greetkeyboard())

    except:
        bot.send_message(message.chat.id, "Город " + city_name + " не найден", kb.greetkeyboard())

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
    bot.send_message(message.chat.id, '\n'.join(onemsg), kb.greetkeyboard(), parse_mode='MarkdownV2')


# Калькулятор
# Текущее значение калькулятора
value = ''
old_value = ''

# Обработчик события вызова калькулятора
@bot.message_handler(commands=['calculator'])
def getMeassage(message):
    global value
    if value == '':
       bot.send_message(message.from_user.id, '0', reply_markup=kb.calckeyboard())
    else:
        bot.send_message(message.from_user.id, value, reply_markup=kb.calckeyboard())
# Программа калькулятора
@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data
    if data == 'C':
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
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=kb.calckeyboard())
            old_value = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup=kb.calckeyboard())
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