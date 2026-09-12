from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.models.weather_reading import WeatherReading
from app.schemas.prediction import PredictionCreate, PredictionUpdate


def create_prediction(
    db: Session,
    prediction: PredictionCreate,
) -> Prediction:
    # Verify that the referenced weather reading exists
    reading = db.query(WeatherReading).filter(WeatherReading.id == prediction.reading_id).first()
    if reading is None:
        raise HTTPException(
            status_code=404,
            detail=f"Weather reading with id {prediction.reading_id} not found",
        )

    data = prediction.model_dump(exclude_unset=True)
    if "created_at" not in data or data["created_at"] is None:
        data["created_at"] = datetime.utcnow()

    db_prediction = Prediction(**data)

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return db_prediction


def get_all_predictions(db: Session) -> list[Prediction]:
    return db.query(Prediction).all()


def get_prediction_by_id(db: Session, prediction_id: int) -> Prediction:
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )
    return prediction


def update_prediction(
    db: Session,
    prediction_id: int,
    prediction_data: PredictionUpdate,
) -> Prediction:
    db_prediction = get_prediction_by_id(db, prediction_id)

    update_data = prediction_data.model_dump(exclude_unset=True)

    # If updating reading_id, verify that the new weather reading exists
    if "reading_id" in update_data and update_data["reading_id"] is not None:
        reading = db.query(WeatherReading).filter(WeatherReading.id == update_data["reading_id"]).first()
        if reading is None:
            raise HTTPException(
                status_code=404,
                detail=f"Weather reading with id {update_data['reading_id']} not found",
            )

    for key, value in update_data.items():
        setattr(db_prediction, key, value)

    db.commit()
    db.refresh(db_prediction)

    return db_prediction


def delete_prediction(db: Session, prediction_id: int) -> dict:
    db_prediction = get_prediction_by_id(db, prediction_id)

    db.delete(db_prediction)
    db.commit()

    return {"message": "Prediction deleted successfully"}

