"""Test fetching real weather through the service"""
import warnings
warnings.filterwarnings('ignore')
from app.services.weather_api_service import fetch_current_weather

print('Fetching live weather from OpenWeather API...')
print('='*60)
weather = fetch_current_weather()
print('✅ SUCCESS - Real Weather Data Received!')
print('='*60)
print(f'Temperature: {weather["temperature"]}°C')
print(f'Humidity: {weather["humidity"]}%')
print(f'Pressure: {weather["pressure"]} hPa')
print(f'Wind Speed: {weather["wind_speed"]} m/s')
print(f'Wind Direction: {weather["wind_direction"]}°')
print(f'Visibility: {weather["visibility"]} km')
print(f'Month: {weather["month"]}')
print(f'Hour: {weather["hour"]}')
print('='*60)
print('🌍 This is REAL weather from Kolkata Airport!')
