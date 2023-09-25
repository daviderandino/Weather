from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
import os
import datetime as dt
import requests


def kelvin_to_celsius(temp):
    return round(temp-273.15,2)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
# API_KEY = ... (hidden)

CITY = "Torino"

# token = ... (hidden)

TOKEN: Final = token
BOT_USERNAME : Final = '@WeatherrApp_bot'

# Commands
async def start_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Benvenuto/a!\nSeleziona la città con /city NOMECITTÀ\ne digita poi /meteo per le informazioni atmosferiche")
    
async def help_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Seleziona la città con /city NOMECITTÀ\ne digita poi /meteo per le informazioni atmosferiche")

async def city_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    global CITY
    global url
    global response
    user_input = update.message.text.split('/city', 1)[-1].strip()
    # Assicurarsi che l'input non sia vuoto prima di modificarlo
    if user_input:
        CITY = user_input  # Imposta la variabile CITY con l'input dell'utente
        await update.message.reply_text(f"Città impostata su {CITY}")
        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
    else:
        await update.message.reply_text("Per favore, specifica una città dopo il comando /city, ad esempio ''/city Torino''")

async def meteo_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    temp_kelvin = response['main']['temp']
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

    await update.message.reply_text("Ecco le condizioni atmosferiche a " + CITY + ":")
    await update.message.reply_text(str(temp_celsius) + "°C")
    await update.message.reply_text(str(humidity) + "%" + " di umidità")
    await update.message.reply_text("Descrizione: " + description)
    await update.message.reply_text("Velocità del vento: " + str(wind_speed) + " m/s")
    await update.message.reply_text("Alba: ore " + str(sunrise_time)[11:])
    await update.message.reply_text("Tramonto: ore " + str(sunset_time)[11:])

# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()
    CITY = processed

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return     
    else:
        response: str = handle_response(text)

    print('Bot:',response)
    await update.message.reply_text(response)

async def error(update: Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')

if __name__ == '__main__':
    
    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    print('Starting bot....')
    response = requests.get(url).json()
    app = Application.builder().token(TOKEN).build()

    # Commands

    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('city',city_command))
    app.add_handler(CommandHandler('meteo',meteo_command))

    # Errors

    app.add_error_handler(error)

    # Polling

    print('Polling...')
    app.run_polling(poll_interval=3)
