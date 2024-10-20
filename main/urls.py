# weather/urls.py
from django.urls import path
from .views import weather_summary_view,set_alert

urlpatterns = [
    path('summary/', weather_summary_view, name='weather-summary'),
    path('set_alert/',set_alert,name="set_alert")
]
