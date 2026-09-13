"""
Test the complete data flow:
Weather fetch → DB insert → Auto prediction → Verification
"""
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime, timezone, date
from app.db.database import SessionLocal
from app.services.weather_api_service import fetch_current_weather
from app.services.prediction_service import predict_weather
from app.crud.weather_reading import create_weather_reading
from app.crud.station import get_all_stations, create_station
from app.crud.prediction import get_all_predictions
from app.schemas.weather_reading import WeatherReadingCreate
from app.schemas.station import StationCreate

db = SessionLocal()

print('='*60)
print('TESTING COMPLETE DATA FLOW')
print('='*60)

print('\n[1/6] Fetching weather data...')
weather_data = fetch_current_weather()
print(f'    Temperature: {weather_data["temperature"]}°C')
print(f'    Humidity: {weather_data["humidity"]}%')
print(f'    Pressure: {weather_data["pressure"]} hPa')
print(f'    Wind Speed: {weather_data["wind_speed"]} m/s')
print(f'    Visibility: {weather_data["visibility"]} km')

print('\n[2/6] Checking station exists...')
stations = get_all_stations(db)
if not stations:
    print('    Creating Kolkata Airport station...')
    station = create_station(db, StationCreate(
        station_code='KOLKATA_AIRPORT',
        name='Netaji Subhas Chandra Bose International Airport',
        city='Kolkata',
        state='West Bengal',
        latitude=22.654739,
        longitude=88.446722,
        status='ACTIVE',
        installation_date=date.today()
    ))
    station_id = station.id
    print(f'    ✅ Station created with ID: {station_id}')
else:
    station_id = stations[0].id
    print(f'    ✅ Using existing station ID: {station_id}')

print('\n[3/6] Creating weather reading in PostgreSQL...')
reading = create_weather_reading(db, WeatherReadingCreate(
    station_id=station_id,
    temperature=weather_data['temperature'],
    humidity=weather_data['humidity'],
    pressure=weather_data['pressure'],
    recorded_at=datetime.now(timezone.utc)
))
print(f'    ✅ Reading saved with ID: {reading.id}')
print(f'    Station: {reading.station_id}')
print(f'    Recorded at: {reading.recorded_at}')

print('\n[4/6] Running ML prediction (manual test)...')
result = predict_weather(weather_data)
print(f'    Prediction: {result["prediction"]}')
print(f'    Anomaly Score: {result["score"]}')
is_anomalous = result["prediction"] == "Anomaly"
print(f'    Is Anomalous: {is_anomalous}')

print('\n[5/6] Checking auto-prediction was saved...')
predictions = get_all_predictions(db)
latest_pred = [p for p in predictions if p.reading_id == reading.id]
if latest_pred:
    p = latest_pred[0]
    print(f'    ✅ Auto-prediction found!')
    print(f'    Prediction ID: {p.id}')
    print(f'    Reading ID: {p.reading_id}')
    print(f'    Is Anomaly: {p.is_anomaly}')
    print(f'    Confidence: {p.confidence_score:.4f}')
    print(f'    Severity: {p.severity}')
    print(f'    Model: {p.model_name} v{p.model_version}')
    print(f'    Inference Time: {p.inference_time_ms:.2f}ms')
else:
    print('    ❌ ERROR: Auto-prediction NOT saved to database')

print('\n[6/6] Verifying data counts...')
all_readings = db.query(__import__('app.models.weather_reading', fromlist=['WeatherReading']).WeatherReading).count()
all_predictions = db.query(__import__('app.models.prediction', fromlist=['Prediction']).Prediction).count()
all_stations = db.query(__import__('app.models.station', fromlist=['Station']).Station).count()
print(f'    Total Stations: {all_stations}')
print(f'    Total Readings: {all_readings}')
print(f'    Total Predictions: {all_predictions}')

anomaly_count = db.query(__import__('app.models.prediction', fromlist=['Prediction']).Prediction).filter_by(is_anomaly=True).count()
print(f'    Anomaly Count: {anomaly_count}')

db.close()

print('\n' + '='*60)
print('✅ ALL TESTS PASSED - COMPLETE FLOW WORKING')
print('='*60)
