from flask import Flask, render_template, request  # Add the missing import
import requests

app = Flask(__name__)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "your api key goes here"  # Make sure api_key.txt contains just the key

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error_message = None  # Initialize error_message to None

    if request.method == 'POST':
        city = request.form['city']
        try:
            url = BASE_URL + "appid=" + API_KEY + "&q=" + city
            response = requests.get(url).json()

            if response['cod'] == 200:
                temperature_kelvin = response['main']['temp']
                temperature_celsius = kelvin_to_celsius(temperature_kelvin)

                weather_data = {
                    'city': response['name'],
                    'temperature': round(temperature_celsius, 2),
                    'description': response['weather'][0]['description'],
                    'humidity': response['main']['humidity'],
                    'wind_speed': round(response['wind']['speed'], 2)
                }
            else:
                error_message = f"Error: {response['message']}"
        except requests.exceptions.RequestException as e:
            error_message = "An error occurred while fetching data. Please try again later."

    return render_template('home.html', weather_data=weather_data, error_message=error_message)

if __name__ == "__main__":
    from flask_app import app
    app.run(host='0.0.0.0')
