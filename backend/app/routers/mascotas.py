from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database

router = APIRouter(
    prefix="/api/mascotas",
    tags=["mascotas"]
)

@router.get("", response_model=List[schemas.MascotaResponse])
def listar_mascotas(db: Session = Depends(database.get_db)):
    return crud.get_mascotas(db)

@router.post("", response_model=schemas.MascotaResponse)
def guardar_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(database.get_db)):
    return crud.create_mascota(db=db, mascota=mascota)
