from django.shortcuts import render
from main.models import DailyWeatherSummary, WeatherData , WeatherAlerts
from django.utils import timezone
import pytz
def set_alert(request):
    if request.method=='POST':
        city = request.POST.get('city')
        condition = request.POST.get('condition')

        if city and condition:
            WeatherAlerts.objects.create(city=city,weathercondition=condition)
            message='Alert Set successfully'
            Class="alert alert-success alert-dismissible fade show"
        else:
            message = 'City and condition are required.'
            Class="alert alert-warning alert-dismissible fade show"
        return render(request,'weather/alertsetmessage.html',{'message':message,'Class':Class})
def weather_summary_view(request):
    today = timezone.now().date()
    summaries = DailyWeatherSummary.objects.filter(date=today)
    weathers = WeatherData.objects.filter(timestamp__date=today)

    # Create a dictionary to map city to its current temperature data
    current_weather = {weather.city: weather for weather in weathers}

    # Add current weather data to each summary object
    for summary in summaries:
        #summary.datetime = summary.datetime.strftime('%Y-%m-%d %H:%M:%S')
        summary.current_weather = current_weather.get(summary.city, None)


    alerts=WeatherAlerts.objects.filter(delete_flag=True)
    alert_string_list=[]
    if alerts:
        for alert in alerts:
            alert_string_list.append(alert.weatherstring)
            alert.delete()
        
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_datetime_ist = timezone.now().astimezone(ist_tz)
    formatted_datetime = current_datetime_ist.strftime('%d-%m-%y ,%H:%M:%S')
    context = {
        'summaries': summaries,
        'currentTime': formatted_datetime,
        'alert_string':alert_string_list
    }

    # Check if the request is from HTMX
    if request.htmx:
        return render(request, 'weather/summary_content.html', context)

    # Default full page render
    return render(request, 'weather/summary.html', context)
