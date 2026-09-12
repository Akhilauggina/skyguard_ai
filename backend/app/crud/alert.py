from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate


def create_alert(db: Session, alert: AlertCreate):
    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alerts(db: Session):
    return db.query(Alert).all()


def get_alert(db: Session, alert_id: int):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(404, "Alert not found")

    return alert


def update_alert(db: Session, alert_id: int, alert_data: AlertUpdate):
    alert = get_alert(db, alert_id)

    update_data = alert_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(alert, key, value)

    db.commit()
    db.refresh(alert)

    return alert


def delete_alert(db: Session, alert_id: int):
    alert = get_alert(db, alert_id)

    db.delete(alert)
    db.commit()

    return {"message": "Alert deleted successfully"}