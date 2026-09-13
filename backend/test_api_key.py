"""Test if OpenWeather API key is active"""
import httpx

response = httpx.get('https://api.openweathermap.org/data/2.5/weather', params={
    'lat': 22.654739,
    'lon': 88.446722,
    'appid': 'a41007ddea848665ed878f665e12db91',
    'units': 'metric'
}, timeout=10.0)

print('Status Code:', response.status_code)
print()

if response.status_code == 200:
    data = response.json()
    print('✅ API KEY IS ACTIVE!')
    print('='*60)
    print(f'Location: {data["name"]}')
    print(f'Country: {data["sys"]["country"]}')
    print(f'Temperature: {data["main"]["temp"]}°C')
    print(f'Feels Like: {data["main"]["feels_like"]}°C')
    print(f'Humidity: {data["main"]["humidity"]}%')
    print(f'Pressure: {data["main"]["pressure"]} hPa')
    print(f'Wind Speed: {data["wind"]["speed"]} m/s')
    print(f'Wind Direction: {data["wind"].get("deg", 0)}°')
    print(f'Weather: {data["weather"][0]["main"]} - {data["weather"][0]["description"]}')
    print(f'Visibility: {data.get("visibility", 0) / 1000} km')
    print(f'Clouds: {data["clouds"]["all"]}%')
    print('='*60)
    print('\n🎉 Real weather data from OpenWeather API!')
else:
    print('❌ API Key not working yet')
    print('Response:', response.json())
    print('\nℹ️  New API keys can take up to 2 hours to activate.')
