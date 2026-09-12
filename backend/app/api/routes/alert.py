from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.alert import (
    create_alert,
    get_alerts,
    get_alert,
    update_alert,
    delete_alert,
)

from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
)

from app.db.dependencies import get_db

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.post("", response_model=AlertResponse, status_code=201)
def create(alert: AlertCreate, db: Session = Depends(get_db)):
    return create_alert(db, alert)


@router.get("", response_model=list[AlertResponse])
def get_all(db: Session = Depends(get_db)):
    return get_alerts(db)


@router.get("/{alert_id}", response_model=AlertResponse)
def get_one(alert_id: int, db: Session = Depends(get_db)):
    return get_alert(db, alert_id)


@router.put("/{alert_id}", response_model=AlertResponse)
def update(
    alert_id: int,
    alert: AlertUpdate,
    db: Session = Depends(get_db),
):
    return update_alert(db, alert_id, alert)


@router.delete("/{alert_id}")
def delete(alert_id: int, db: Session = Depends(get_db)):
    return delete_alert(db, alert_id)