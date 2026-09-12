from fastapi import APIRouter, Depends
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

