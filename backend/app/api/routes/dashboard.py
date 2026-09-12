from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.dashboard import get_dashboard_stats
from app.db.dependencies import get_db
from app.schemas.dashboard import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("", response_model=DashboardResponse)
def dashboard(
    db: Session = Depends(get_db),
):
    return get_dashboard_stats(db)