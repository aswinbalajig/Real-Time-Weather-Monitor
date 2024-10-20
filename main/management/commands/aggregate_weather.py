from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Min
from main.models import WeatherData, DailyWeatherSummary
from django.utils import timezone
from collections import Counter
import pytz

CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

class Command(BaseCommand):
    help = 'Generate daily weather summaries for each city'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        for city in CITIES:
            daily_weather = WeatherData.objects.filter(city=city, timestamp__date=today)
            if daily_weather.exists():
                avg_temp = daily_weather.aggregate(Avg('temp'))['temp__avg']
                max_temp = daily_weather.aggregate(Max('temp'))['temp__max']
                min_temp = daily_weather.aggregate(Min('temp'))['temp__min']
                weather_conditions = daily_weather.values_list('main', flat=True)
                dominant_condition = Counter(weather_conditions).most_common(1)[0][0]

                DailyWeatherSummary.objects.update_or_create(
                    city=city,
                    defaults={
                        'avg_temp': avg_temp,
                        'max_temp': max_temp,
                        'min_temp': min_temp,
                        'dominant_condition': dominant_condition
                    }
                )
                self.stdout.write(f"Daily summary for {city} on {today} generated.")
