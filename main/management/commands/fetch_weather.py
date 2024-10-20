import requests
from django.core.management.base import BaseCommand
from main.models import WeatherData,WeatherAlerts
from django.utils import timezone
from django.conf import settings  # Import settings
from django.core.exceptions import ImproperlyConfigured
import datetime
import pytz  # Import pytz for timezone conversion

CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
API_URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

class Command(BaseCommand):
    help = 'Fetch weather data from OpenWeather API for Indian cities'

    def handle(self, *args, **kwargs):
        api_key = settings.API_KEY  

        if not api_key:
            raise ImproperlyConfigured("API key not set in settings.")

        for city in CITIES:
            response = requests.get(API_URL.format(city=city, api_key=api_key))
            data = response.json()

            self.stdout.write(f"Response for {city}: {data}")
            def get_weather_condition_by_id(weather_id):
                if 200 <= weather_id <= 232:
                    return "Thunderstorm"
                elif 300 <= weather_id <= 321:
                    return "Drizzle"
                elif 500 <= weather_id <= 531:
                    return "Rain"
                elif 600 <= weather_id <= 622:
                    return "Snow"
                elif 701 <= weather_id <= 781:
                    return "Windy"
                elif weather_id == 800:
                    return "Clear"
                elif 801 <= weather_id <= 804:
                    return "Clouds"
                else:
                    return "Unknown"

            

            if 'main' in data:
                temp_celsius = kelvin_to_celsius(data['main']['temp'])
                feels_like_celsius = kelvin_to_celsius(data['main']['feels_like'])
                weather_main = data['weather'][0]['main']
                weather_id = data['weather'][0]['id']
                weather_condition=get_weather_condition_by_id(weather_id)
                
                #Alert Checking :
                alerts=WeatherAlerts.objects.filter(city=city , weathercondition=weather_condition)
                for alert in alerts:
                    alert.weatherstring=f"ALERT! {weather_condition} in {city}"
                    alert.delete_flag=True
                    alert.save()

                if 'dt' in data:
                    dt = data['dt']
                    # Converting the UNIX timestamp to UTC first
                    utc_timestamp = datetime.datetime.fromtimestamp(dt, tz=datetime.timezone.utc)
                    
                    # Converting UTC to IST
                    ist_tz = pytz.timezone('Asia/Kolkata')
                    timestamp = utc_timestamp.astimezone(ist_tz)
                    print(f'timestamp:{timestamp}')
                else:
                    # If 'dt' is not present, use the current time in IST
                    timestamp = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
                print(f'timestamp:{timestamp}')

                WeatherData.objects.create(
                    city=city,
                    main=weather_main,
                    temp=temp_celsius,
                    feels_like=feels_like_celsius,
                    timestamp=timestamp,
                    weather_id=weather_id
                )
                self.stdout.write(f"Weather data for {city} at {timestamp} recorded.")
            else:
                self.stdout.write(f"Error: 'main' not found in the response for {city}. Response data: {data}")
