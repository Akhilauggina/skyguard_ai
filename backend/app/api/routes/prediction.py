from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.prediction import (
    create_prediction,
    delete_prediction,
    get_all_predictions,
    get_prediction_by_id,
    update_prediction,
)
from app.db.dependencies import get_db
from app.schemas.prediction import (
    PredictRequest,
    PredictResponse,
    PredictionCreate,
    PredictionResponse,
    PredictionUpdate,
)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "",
    response_model=PredictionResponse,
    status_code=201,
    summary="Create a new prediction",
)
def create_new_prediction(
    prediction: PredictionCreate,
    db: Session = Depends(get_db),
):
    return create_prediction(db, prediction)


@router.get(
    "",
    response_model=list[PredictionResponse],
    summary="Get all predictions",
)
def read_all_predictions(
    db: Session = Depends(get_db),
):
    return get_all_predictions(db)


@router.post(
    "/predict",
    response_model=PredictResponse,
    summary="Run ML prediction on weather data",
    description=(
        "Submit weather features (temperature, humidity, pressure, etc.) "
        "and get back an anomaly prediction from the Isolation Forest model."
    ),
)
def predict_weather_anomaly(payload: PredictRequest):
    """Manually test the ML model with custom weather data."""
    import time

    try:
        from app.services.prediction_service import predict_weather
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"ML model not available: {exc}",
        )

    start = time.perf_counter()
    result = predict_weather(payload.model_dump())
    elapsed_ms = (time.perf_counter() - start) * 1000

    return PredictResponse(
        prediction=result["prediction"],
        score=result["score"],
    )


@router.get(
    "/{id}",
    response_model=PredictionResponse,
    summary="Get a prediction by ID",
)
def read_prediction(
    id: int,
    db: Session = Depends(get_db),
):
    return get_prediction_by_id(db, id)


@router.put(
    "/{id}",
    response_model=PredictionResponse,
    summary="Update a prediction by ID",
)
def update_existing_prediction(
    id: int,
    prediction: PredictionUpdate,
    db: Session = Depends(get_db),
):
    return update_prediction(db, id, prediction)


@router.delete(
    "/{id}",
    summary="Delete a prediction by ID",
)
def delete_existing_prediction(
    id: int,
    db: Session = Depends(get_db),
):
    return delete_prediction(db, id)

