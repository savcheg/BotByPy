import re

import keyboards as kb
import telebot, requests


# TOKEN
bot = telebot.TeleBot("1868448936:AAGnebbrW9BkMt-LrRY0CN038s3f7mK-HLA")


# Обработчик события приветствия
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name, reply_markup = kb.greetkeyboard())

@bot.message_handler(content_types= ['text'])
def greeting(message):
    if message.text == 'Узнать погоду':
        setlocation(message)
    elif message.text == 'Калькулятор':
        start_calc(message)
    elif message.text == 'Графика':
        magictext(message)


# Погода
url = 'http://api.openweathermap.org/data/2.5/weather'
api_weather = 'f3ed8e4e21b60cbface5df90ff430d57'
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


        bot.send_message(message.chat.id, "🌡В городе " + str(weather["name"]) + " температура " + str(
            float(weather["main"]['temp'])) + " °C\n" +
                         "💨Скорость ветра " + str(float(weather['wind']['speed'])) + " м/с\n" +
                         "💦Влажность " + str(int(weather['main']['humidity'])) + " %\n", kb.greetkeyboard())

    except:
        bot.send_message(message.chat.id, "Город " + city_name + " не найден", kb.greetkeyboard())

# Перевод слов в символы
alphabet =      {'А' : 0, 'Б' : 1, 'В' : 2, 'Г' : 3, 'Д' : 4, 'Е' : 5, 'Ж' : 6, 'З' : 7, 'И' : 8, 'К' : 9,
                 'Л' : 10, 'М' : 11, 'Н' : 12, 'О' : 13, 'П' : 14, 'Р' : 15, 'С' : 16, 'Т' : 17, 'У' : 18, 'Ф' : 19,
                 'Х' : 20, 'Ц' : 21, 'Ч' : 22, 'Ш' : 23, 'Щ' : 24, 'Ъ' : 25, 'Ы' : 26, 'Ь' : 27, 'Э' : 28, 'Ю' : 29,
                 'Я' : 30}

# Вводим слово
@bot.message_handler(commands=['graphics'])
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
@bot.message_handler(commands=['calculator'])
def start_calc(message):
    primer = bot.send_message(message.chat.id, "Введите пример >>")
    bot.register_next_step_handler(primer, calculator)


def calculator(message):
    s = message.text
    s = re.sub(r"\s*", "", s)
    s1 = ""
    queue = []
    stack = []
    for i in range(0, len(s)):
        if (s[i].isdigit()):
            s1 = str(s1) + str(s[i])
        else:
            if (len(s1) > 0):
                queue.append(s1)
                s1 = ""
            if (len(stack) == 0 or stack[0] == "("):
                stack.insert(0, s[i])
            elif (s[i] in "*/^" and stack[0] in "+-"):
                stack.insert(0, s[i])
            elif (s[i] in "+-*/^" and stack[0] in "+-*/^"):
                if (s[i] in "+-" and stack[0] in "^*/+-"):
                    while (len(stack) > 0 and not (stack[0] in "(")):
                        queue.append(stack.pop(0))
                    stack.insert(0, s[i])
                elif (s[i] in "*/^" and stack[0] in "*/^"):
                    while (len(stack) > 0 and not (stack[0] in "+-(")):
                        queue.append(stack.pop(0))
                    stack.insert(0, s[i])
            elif (s[i] == "("):
                stack.insert(0, "(")
            elif (s[i] == ")"):
                while (len(stack) > 0 and stack[0] != "("):
                    queue.append(stack.pop(0))
                if (len(stack) > 0): stack.pop(0)
    if (len(s1) > 0): queue.append(s1)
    while (len(stack) > 0): queue.append(stack.pop(0))
    stack1 = []
    for i in queue:
        if (i.isdigit()):
            stack1.insert(0, i)
        elif (i in "+-*/^"):
            a = int(stack1.pop(0))
            b = int(stack1.pop(0))
            res = 0
            if (i == "+"): res = b + a
            if (i == "-"): res = b - a
            if (i == "*"): res = b * a
            if (i == "/"): res = b / a
            if (i == "^"): res = pow(b, a)
            stack1.insert(0, res)
    bot.send_message(message.chat.id, 'Вот тебе ответ:')
    bot.send_message(message.chat.id, str(res), reply_markup=kb.greetkeyboard())


# Запуск бота
#bot.polling(none_stop=True, interval=0)
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            telebot.logger.error(ex)
