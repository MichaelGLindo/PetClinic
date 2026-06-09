from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database
from app.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/api/turnos",
    tags=["turnos"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[schemas.TurnoResponse])
def listar_turnos(
    mascota_id: int | None = None,
    mascotaId: int | None = None,
    db: Session = Depends(database.get_db)
):
    m_id = mascota_id if mascota_id is not None else mascotaId
    return crud.get_turnos(db, mascota_id=m_id)

@router.post("", response_model=schemas.TurnoResponse)
def guardar_turno(turno: schemas.TurnoCreate, db: Session = Depends(database.get_db)):
    # Verify mascota exists if specified
    pet_id = None
    if turno.mascota_id is not None:
        pet_id = turno.mascota_id
    elif turno.mascotaId is not None:
        pet_id = turno.mascotaId
    elif turno.mascota:
        if isinstance(turno.mascota, dict):
            pet_id = turno.mascota.get("id")
        elif hasattr(turno.mascota, "id"):
            pet_id = getattr(turno.mascota, "id")

    if pet_id is not None:
        db_mascota = crud.get_mascota(db, id=pet_id)
        if not db_mascota:
            raise HTTPException(status_code=400, detail="La mascota especificada no existe")

    return crud.create_turno(db=db, turno=turno)

@router.get("/proximos", response_model=List[schemas.TurnoResponse])
def listar_turnos_proximos(db: Session = Depends(database.get_db)):
    return crud.get_turnos_proximos(db)

@router.get("/{id}", response_model=schemas.TurnoResponse)
def obtener_turno(id: int, db: Session = Depends(database.get_db)):
    db_turno = crud.get_turno(db, id=id)
    if not db_turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return db_turno

@router.put("/{id}", response_model=schemas.TurnoResponse)
def actualizar_turno(id: int, turno: schemas.TurnoUpdate, db: Session = Depends(database.get_db)):
    # Verify mascota exists if specified
    pet_id = None
    if turno.mascota_id is not None:
        pet_id = turno.mascota_id
    elif turno.mascotaId is not None:
        pet_id = turno.mascotaId
    elif turno.mascota:
        if isinstance(turno.mascota, dict):
            pet_id = turno.mascota.get("id")
        elif hasattr(turno.mascota, "id"):
            pet_id = getattr(turno.mascota, "id")

    if pet_id is not None:
        db_mascota = crud.get_mascota(db, id=pet_id)
        if not db_mascota:
            raise HTTPException(status_code=400, detail="La mascota especificada no existe")

    db_turno = crud.update_turno(db, id=id, turno=turno)
    if not db_turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return db_turno

@router.delete("/{id}")
def eliminar_turno(id: int, db: Session = Depends(database.get_db)):
    success = crud.delete_turno(db, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return {"message": "Turno eliminado correctamente"}
