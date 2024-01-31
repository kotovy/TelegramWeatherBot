import telebot
from telebot import types
import requests

telegram_token = "YouTelegramToken"

bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    bot.send_message(message.chat.id, f"Hello, {user.first_name}!", reply_markup=get_keyboard())

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "This bot provides weather information. Use /weather <city> to get the weather.")

@bot.message_handler(commands=['weather'])
def handle_weather(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Use the /weather <city> command to get the weather.")
        return

    city = " ".join(message.text.split()[1:])
    weather_data = get_weather(city)

    if weather_data:
        bot.send_message(message.chat.id, f"Weather in {city}: {weather_data}")
    else:
        bot.send_message(message.chat.id, "Failed to get weather information. Please try again.")

def get_weather(city: str) -> str:
    api_key = "YouoOpenweathermapToken"
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature_kelvin = data['main']['temp']
        
        temperature_celsius = temperature_kelvin - 273.15

        return f"{weather_description.capitalize()}. Temperature: {temperature_celsius:.2f}°C"
    except Exception as e:
        print(f"Error while retrieving weather data: {e}")
        return None

def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    help_button = types.KeyboardButton("/help")
    keyboard.add(help_button)
    return keyboard

if __name__ == "__main__":
    bot.polling(none_stop=True)
