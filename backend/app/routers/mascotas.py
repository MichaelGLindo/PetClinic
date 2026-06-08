from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database

router = APIRouter(
    prefix="/api/mascotas",
    tags=["mascotas"]
)

@router.get("", response_model=List[schemas.MascotaResponse])
def listar_mascotas(
    dueno_cedula: str | None = None,
    cedulaDueno: str | None = None,
    db: Session = Depends(database.get_db)
):
    cedula = dueno_cedula or cedulaDueno
    return crud.get_mascotas(db, dueno_cedula=cedula)

@router.post("", response_model=schemas.MascotaResponse)
def guardar_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(database.get_db)):
    # Verify owner exists if specified
    owner_cedula = None
    if mascota.dueno_cedula:
        owner_cedula = mascota.dueno_cedula
    elif mascota.cedulaDueno:
        owner_cedula = mascota.cedulaDueno
    elif mascota.dueno and hasattr(mascota.dueno, 'cedula'):
        owner_cedula = mascota.dueno.cedula

    if owner_cedula:
        db_dueno = crud.get_dueno(db, cedula=owner_cedula)
        if not db_dueno:
            raise HTTPException(status_code=400, detail="El dueño especificado no existe")

    return crud.create_mascota(db=db, mascota=mascota)

@router.get("/buscar/max", response_model=List[schemas.MascotaResponse])
def obtener_mascota_max_edad(db: Session = Depends(database.get_db)):
    return crud.get_mascota_max_edad(db)

@router.get("/{id}", response_model=schemas.MascotaResponse)
def obtener_mascota(id: int, db: Session = Depends(database.get_db)):
    db_mascota = crud.get_mascota(db, id=id)
    if not db_mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return db_mascota

@router.put("/{id}", response_model=schemas.MascotaResponse)
def actualizar_mascota(id: int, mascota: schemas.MascotaUpdate, db: Session = Depends(database.get_db)):
    # Verify owner exists if specified
    owner_cedula = None
    if mascota.dueno_cedula is not None:
        owner_cedula = mascota.dueno_cedula
    elif mascota.cedulaDueno is not None:
        owner_cedula = mascota.cedulaDueno
    elif mascota.dueno and hasattr(mascota.dueno, 'cedula'):
        owner_cedula = mascota.dueno.cedula

    if owner_cedula:
        db_dueno = crud.get_dueno(db, cedula=owner_cedula)
        if not db_dueno:
            raise HTTPException(status_code=400, detail="El dueño especificado no existe")

    db_mascota = crud.update_mascota(db, id=id, mascota=mascota)
    if not db_mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return db_mascota

@router.delete("/{id}")
def eliminar_mascota(id: int, db: Session = Depends(database.get_db)):
    success = crud.delete_mascota(db, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return {"message": "Mascota eliminada correctamente"}
