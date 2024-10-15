import telebot
import requests
import json
import time

token = ''

bot = telebot.TeleBot(token)

api_key = ''


HELP = '''
Список доступных команд:
/city N - Показать погоду в городе N
/help - Напечатать help
'''


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['city'])
def find_city(message):
    _, city = message.text.split(maxsplit=1)

    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}')
    name = response.json()[0].get('local_names').get('ru')
    latitude = response.json()[0].get('lat')
    longitude = response.json()[0].get('lon')
    coordinates = (latitude, longitude)

    bot.send_message(message.chat.id, f'Найден город: {name}, координаты: {coordinates}')
    time.sleep(1)

    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&appid={api_key}')
    temp = round(-273 + response.json().get('main').get('temp'), 1)
    feels_like = round(-273 + response.json().get('main').get('feels_like'), 1)
    wind_speed = round(response.json().get('wind').get('speed'), 1)
    clouds = response.json().get('clouds').get('all')
    pressure = response.json().get('main').get('grnd_level')

    bot.send_message(message.chat.id, f'Сейчас в городе {name}: температура воздуха: {temp} ℃, ощущается как: {feels_like} ℃,  скорость ветра: {wind_speed} м/с, облачность: {clouds} %, атмосферное давление: {pressure} мм. рт. ст.')


bot.polling(none_stop=True)
