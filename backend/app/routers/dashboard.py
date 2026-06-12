from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

from app.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/stats", response_model=schemas.DashboardStatsResponse)
def obtener_estadisticas(db: Session = Depends(database.get_db)):
    return crud.get_dashboard_stats(db)
