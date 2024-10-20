from django.core.management.base import BaseCommand
from django.core.management import call_command
import time

class Command(BaseCommand):
    help = 'Fetch weather data and generate daily summaries for each city repeatedly'

    def handle(self, *args, **kwargs):
        while True:
            # Fetch weather data
            self.stdout.write("Fetching weather data...")
            call_command('fetch_weather')

            # Aggregate weather data
            self.stdout.write("Generating daily weather summaries...")
            call_command('aggregate_weather')

            # Wait for a specified interval before repeating (e.g., every 10 seconds)
            time.sleep(30)  # Adjust the sleep time as needed