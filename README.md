## Project Overview: Real-Time Weather Monitoring System

This project is a real-time weather monitoring system that retrieves and stores weather data for various cities. It utilizes the OpenWeatherMap API to fetch current weather information and stores it in a database for analysis and visualization.

**Data Model**

The system utilizes three main models to represent different aspects of weather data:

| Model Name | Attributes | Description |
|---|---|---|
| WeatherData |  * city (CharField) <br> * main (CharField) <br> * temp (DecimalField) <br> * feels_like (DecimalField) <br> * timestamp (DateTimeField) <br> * weather_id (IntegerField) | Stores current weather data for a specific city. <br> * city: Name of the city. <br> * main: Main weather condition (e.g., Rain, Clear). <br> * temp: Current temperature in Celsius. <br> * feels_like: Perceived temperature in Celsius. <br> * timestamp: Date and time when the data was fetched. <br> * weather_id: Numerical weather condition code. |
| DailyWeatherSummary | * city (CharField) <br> * date (DateField) <br> * avg_temp (DecimalField) <br> * max_temp (DecimalField) <br> * min_temp (DecimalField) <br> * dominant_condition (CharField) | Stores daily weather summaries for a city. <br> * city: Name of the city. <br> * date: Date for which the summary is generated. <br> * avg_temp: Average temperature for the day (Celsius). <br> * max_temp: Maximum temperature for the day (Celsius). <br> * min_temp: Minimum temperature for the day (Celsius). <br> * dominant_condition: Most frequent weather condition for the day. |
| WeatherAlerts | * city (CharField) <br> * weathercondition (CharField) <br> * weatherstring (CharField) <br> * delete_flag (BooleanField) | Stores user-defined weather alerts for specific cities and conditions. <br> * city: Name of the city for the alert. <br> * weathercondition: Specific weather condition to trigger the alert. <br> * weatherstring: Message or notification string for the alert. <br> * delete_flag: Indicates if the alert should be displayed (False) or marked for removal (True). |

**Data Flow**

1. **Data Fetching:**
    * A management command (`run_weather_tasks.py`) runs periodically (every 2 minutes).
    * Within the command, separate tasks are called for fetching and summarizing data.
    * The fetching task retrieves current weather data from OpenWeatherMap for configured cities.
    * The retrieved data is stored in the `WeatherData` model.

2. **Data Summarization:**
    * The summarization task calculates daily weather summaries for each city.
    * It analyzes `WeatherData` entries for the current date and calculates:
        * Average temperature
        * Maximum temperature
        * Minimum temperature
        * Dominant weather condition
    * The summary is stored in the `DailyWeatherSummary` model.

3. **Alert Management:**
    * Users can set alerts for specific weather conditions in specific cities.
    * Alerts are stored in the `WeatherAlerts` model with:
        * City name
        * Triggering weather condition
        * Alert message
        * Deletion flag (initially set to False)
    * During data fetching, the system checks if the current weather condition matches any existing alerts for that city.
    * If a match is found, an alert message string is generated and stored in the corresponding `WeatherAlerts` record.
    * The deletion flag for the alert is set to True, indicating it's ready for removal.

4. **Data Display and Interface:**
    * The user interface retrieves weather data from the database (every 1 minute, independent of data fetching).
    * It utilizes HTMX for dynamic updates.
    * The interface displays current weather information for selected cities.
    * A separate mechanism exists for managing user-defined alerts.
    * When the interface receives a request (presumably triggered by user interaction), it:
        * Filters for `WeatherAlerts` records marked for deletion (delete_flag=True)
        * Retrieves the alert message string for each filtered record.
        * Displays the retrieved alert messages to the user.
        * Simultaneously removes the corresponding alert records from the database by setting the deletion flag to True.

**Overall, this system provides a comprehensive real-time weather monitoring solution with features like:**

* Continuous data fetching and storage from OpenWeatherMap API.
* Daily weather summaries for in-depth analysis.
* Customizable weather alerts for user notification.


## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**

Clone the GitHub repository to your local machine using the following command:

```bash
git clone https://github.com/your_username/your_repo_name.git
```

2. **Navigate to the Project Directory**

Navigate to the project directory after cloning:

```bash
cd your_repo_name
```

3. **Install Dependencies**

Use Pipenv to install the required dependencies specified in the Pipfile:
if pipenv is not present , use the command

``` bash
pip install pipenv
```
if present , then 

```bash
pipenv install
```

4. **Generate a Secret Key**

Generate a secure `SECRET_KEY` for your Django project by running this Python script:

```python
import secrets
print(secrets.token_urlsafe(50))
```

Copy the generated key.

5. **Set the Secret Key**

There are two ways to set your secret key:

**Option 1: Edit settings.py**

Replace the `SECRET_KEY` in `settings.py` with your newly generated key:

```python
SECRET_KEY = 'your_generated_secret_key'
```

**Option 2: Use an environment variable**

Create a `.env` file in the root directory and add the key:

```
SECRET_KEY=your_generated_secret_key
```

Then, ensure `settings.py` is set to load the key from the environment:

```python
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
```

6. **Get an API Key from OpenWeatherMap**

To use weather-related features in the project, you need to obtain an API key from OpenWeatherMap:

* Go to OpenWeatherMap and create an account.
* Once registered, navigate to the API keys section in your account.
* Generate a new API key and copy it.

7. **Set the API Key**

After obtaining your API key, you can set it in your project:

**Option 1: Edit settings.py**

Add the API key directly in `settings.py`:

```python
API_KEY = 'your_openweathermap_api_key'
```

**Option 2: Use an environment variable**

Add the API key to your `.env` file:

```
API_KEY=your_openweathermap_api_key
```

Then, ensure `settings.py` is set to load it:

```python
API_KEY = os.getenv('API_KEY')
```

8. **Apply Database Migrations**

Run the following command to apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

9. **Start the Development Server**

run the development server in seperate terminal:

```bash
python manage.py runserver
```

9. **Start the background taskss**

run the background tasks in another seperate terminal:

```bash
python manage.py run_weather_tasks
```
**check pipfile for all dependencies , change the versions if you want for compatability**

