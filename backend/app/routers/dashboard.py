from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"]
)

@router.get("/stats", response_model=schemas.DashboardStatsResponse)
def obtener_estadisticas(db: Session = Depends(database.get_db)):
    return crud.get_dashboard_stats(db)
