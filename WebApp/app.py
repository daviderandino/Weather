from flask import Flask, render_template, jsonify, request
import requests
import datetime as dt

app = Flask(__name__)

def kelvin_to_celsius(temp):
    return round(temp-273.15,2)

stringa = ""

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
# API_KEY = "..."   hidden

@app.route('/')
def home():
    return render_template('index.html')

# Funzione Python che restituirà una stringa
def get_string_from_python():
    return stringa

# Endpoint per ottenere la stringa
@app.route('/get_string', methods=['GET'])
def get_string():
    string_value = get_string_from_python()
    return jsonify({'value': string_value})

# Endpoint per memorizzare l'input utente
@app.route('/store_input', methods=['POST'])
def store_input():
    global stringa
    data = request.get_json()
    city = data.get('city', '')  # Ottieni l'input utente dalla richiesta JSON
    print(city)

    # Fai qualcosa con l'input utente, ad esempio memorizzalo in una variabile globale o un database
    # Puoi anche restituire una risposta JSON di conferma se necessario

    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    if response['cod'] == '404':
        stringa = "Città non valida!"
        return jsonify({'message': 'Error 404'})
    
    else:
        temp_kelvin = response['main']['temp']
        temp_celsius = kelvin_to_celsius(temp_kelvin)
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

        stringa = "Temperatura: " + str(temp_celsius) + "°C\n" + \
            "Umidità: " + str(humidity) + "%\n" + \
            "Velocità del vento: " + str(wind_speed) + " m/s\n" + \
            "Descrizione: " + description + "\n" + \
            "Orario alba: " + str(sunrise_time)[11:] + "\n" + \
            "Orario tramonto: " + str(sunset_time)[11:]
        return jsonify({'message': 'Input utente memorizzato correttamente'})

if __name__ == '__main__':
    app.run(debug=True)
