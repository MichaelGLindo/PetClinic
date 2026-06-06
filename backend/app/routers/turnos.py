from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database

router = APIRouter(
    prefix="/api/turnos",
    tags=["turnos"]
)

@router.get("", response_model=List[schemas.TurnoResponse])
def listar_turnos(db: Session = Depends(database.get_db)):
    return crud.get_turnos(db)

@router.post("", response_model=schemas.TurnoResponse)
def guardar_turno(turno: schemas.TurnoCreate, db: Session = Depends(database.get_db)):
    return crud.create_turno(db=db, turno=turno)
