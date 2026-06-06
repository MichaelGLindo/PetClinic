from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database

router = APIRouter(
    prefix="/api/duenos",
    tags=["duenos"]
)

@router.get("", response_model=List[schemas.DuenoResponse])
def listar_duenos(db: Session = Depends(database.get_db)):
    return crud.get_duenos(db)

@router.post("", response_model=schemas.DuenoResponse)
def guardar_dueno(dueno: schemas.DuenoCreate, db: Session = Depends(database.get_db)):
    return crud.create_dueno(db=db, dueno=dueno)
