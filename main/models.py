from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    main = models.CharField(max_length=50)  # e.g., Rain, Clear
    temp = models.DecimalField(max_digits=5, decimal_places=2)  # Temperature in Celsius
    feels_like = models.DecimalField(max_digits=5, decimal_places=2)  # Perceived temperature in Celsius
    timestamp = models.DateTimeField()  # Timestamp of the weather data
    weather_id=models.IntegerField()

    def __str__(self):
        return f'{self.city} - {self.temp}°C - {self.main}'


class DailyWeatherSummary(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now().date())
    avg_temp = models.DecimalField(max_digits=5, decimal_places=2)
    max_temp = models.DecimalField(max_digits=5, decimal_places=2)
    min_temp = models.DecimalField(max_digits=5, decimal_places=2)
    dominant_condition = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.city} - {self.date} - Avg: {self.avg_temp}°C"

class WeatherAlerts(models.Model):
    city=models.CharField(max_length=100)
    weathercondition=models.CharField(max_length=50)
    weatherstring=models.CharField(max_length=500,null=True)
    delete_flag=models.BooleanField(default=False)

