from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "ml_models"

model = joblib.load(MODEL_DIR / "iforest.pkl")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")
feature_columns = joblib.load(MODEL_DIR / "features.pkl")


def predict_weather(data: dict):

    df = pd.DataFrame([data])

    df = df[feature_columns]

    scaled = scaler.transform(df)

    prediction = model.predict(scaled)[0]

    score = float(model.decision_function(scaled)[0])

    return {
        "prediction": "Normal" if prediction == 1 else "Anomaly",
        "score": round(score, 4)
    }