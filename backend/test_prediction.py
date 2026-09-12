from app.services.prediction_service import predict_weather

sample = {
    "temperature": 31.2,
    "humidity": 72,
    "pressure": 1008,
    "wind_speed": 2.5,
    "wind_direction": 320,
    "visibility": 9000,
    "month": 9,
    "hour": 14,
}

print(predict_weather(sample))