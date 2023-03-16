import requests
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀',
              801: '🌤',
              802: '☁',
              803: '☁',
              804: '☁'}

WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
def get_weather(lat, lon):
    WEATHER_TOKEN = os.environ['WEATHER_TOKEN']
    params = {
        'appid': WEATHER_TOKEN,
        'lat': lat, 
        'lon': lon,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(WEATHER_URL, params=params).json()
    message = f'Погода в {response["name"]}'
    message += f'\nТемпература {response["main"]["temp"]}'
    message += f'\nОщущается как {response["main"]["feels_like"]}'
    message += f'\n{EMOJI_CODE[response["cod"]]} {response["weather"][0]["description"]}'
    return message

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton('Узнать погоду', request_location=True))
    keyboard.add(KeyboardButton('О проекте'))
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    weather = get_weather(message.location.latitude, message.location.longitude)
    bot.send_message(message.chat.id, weather)

@bot.message_handler(regexp='О проекте')
def about(message):
    bot.send_message(message.chat.id, f'Я бот, который помогает узнает погоду. Я беру погоду с сайта{WEATHER_URL}')


if __name__=='__main__':
    bot.infinity_polling()
