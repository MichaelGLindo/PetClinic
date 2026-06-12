from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database, models
from app.auth_dependencies import get_current_user
from app.roles import require_role

router = APIRouter(
    prefix="/api/historiales",
    tags=["historiales"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[schemas.HistorialClinicoResponse])
def listar_historiales(
    mascota_id: int | None = None,
    mascotaId: int | None = None,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    m_id = mascota_id if mascota_id is not None else mascotaId
    if current_user.rol != "ADMIN":
        my_pets = db.query(models.Mascota).filter(models.Mascota.dueno_cedula == current_user.dueno_cedula).all()
        my_pet_ids = [p.id for p in my_pets]
        if m_id is not None:
            if m_id not in my_pet_ids:
                return []
            return crud.get_historiales(db, mascota_id=m_id)
        if not my_pet_ids:
            return []
        return db.query(models.HistorialClinico).filter(models.HistorialClinico.mascota_id.in_(my_pet_ids)).order_by(models.HistorialClinico.fecha.desc()).all()
        
    return crud.get_historiales(db, mascota_id=m_id)

@router.post("", response_model=schemas.HistorialClinicoResponse)
def guardar_historial(
    historial: schemas.HistorialClinicoCreate,
    db: Session = Depends(database.get_db),
    admin = Depends(require_role("ADMIN"))
):
    pet_id = None
    if historial.mascota_id is not None:
        pet_id = historial.mascota_id
    elif historial.mascotaId is not None:
        pet_id = historial.mascotaId

    if pet_id is not None:
        db_mascota = crud.get_mascota(db, id=pet_id)
        if not db_mascota:
            raise HTTPException(status_code=400, detail="La mascota especificada no existe")

    return crud.create_historial(db=db, historial=historial)

@router.get("/{id}", response_model=schemas.HistorialClinicoResponse)
def obtener_historial(
    id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    db_historial = crud.get_historial(db, id=id)
    if not db_historial:
        raise HTTPException(status_code=404, detail="Historial clínico no encontrado")
    if current_user.rol != "ADMIN":
        if not db_historial.mascota or db_historial.mascota.dueno_cedula != current_user.dueno_cedula:
            raise HTTPException(status_code=403, detail="No autorizado a ver este historial clínico")
    return db_historial

@router.put("/{id}", response_model=schemas.HistorialClinicoResponse)
def actualizar_historial(
    id: int,
    historial: schemas.HistorialClinicoUpdate,
    db: Session = Depends(database.get_db),
    admin = Depends(require_role("ADMIN"))
):
    pet_id = None
    if historial.mascota_id is not None:
        pet_id = historial.mascota_id
    elif historial.mascotaId is not None:
        pet_id = historial.mascotaId

    if pet_id is not None:
        db_mascota = crud.get_mascota(db, id=pet_id)
        if not db_mascota:
            raise HTTPException(status_code=400, detail="La mascota especificada no existe")

    db_historial = crud.update_historial(db, id=id, historial=historial)
    if not db_historial:
        raise HTTPException(status_code=404, detail="Historial clínico no encontrado")
    return db_historial

@router.delete("/{id}")
def eliminar_historial(
    id: int,
    db: Session = Depends(database.get_db),
    admin = Depends(require_role("ADMIN"))
):
    success = crud.delete_historial(db, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Historial clínico no encontrado")
    return {"message": "Historial clínico eliminado correctamente"}
