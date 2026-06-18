from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from app import crud, schemas, database, models
from app.auth_dependencies import get_current_user
from app.roles import require_role

router = APIRouter(
    prefix="/api/turnos",
    tags=["turnos"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[schemas.TurnoResponse])
def listar_turnos(
    mascota_id: int | None = None,
    mascotaId: int | None = None,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    m_id = mascota_id if mascota_id is not None else mascotaId
    if current_user.rol != "ADMIN":
        # Filter turnos by current user's pets
        my_pets = db.query(models.Mascota).filter(models.Mascota.dueno_cedula == current_user.dueno_cedula).all()
        my_pet_ids = [p.id for p in my_pets]
        if m_id is not None:
            if m_id not in my_pet_ids:
                return []
            return crud.get_turnos(db, mascota_id=m_id)
        if not my_pet_ids:
            return []
        return db.query(models.Turno).filter(models.Turno.mascota_id.in_(my_pet_ids)).all()
        
    return crud.get_turnos(db, mascota_id=m_id)

@router.post("", response_model=schemas.TurnoResponse)
def guardar_turno(
    turno: schemas.TurnoCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    pet_id = None
    if turno.mascota_id is not None:
        pet_id = int(turno.mascota_id)
    elif turno.mascotaId is not None:
        pet_id = int(turno.mascotaId)
    elif turno.mascota:
        if isinstance(turno.mascota, dict):
            pet_id = int(turno.mascota.get("id", 0))
        elif hasattr(turno.mascota, "id"):
            pet_id = int(getattr(turno.mascota, "id"))

    if not pet_id:
        raise HTTPException(status_code=400, detail="Debe especificar una mascota")

    db_mascota = crud.get_mascota(db, id=pet_id)
    if not db_mascota:
        raise HTTPException(status_code=400, detail="La mascota especificada no existe")

    if current_user.rol != "ADMIN":
        if db_mascota.dueno_cedula != current_user.dueno_cedula:
            raise HTTPException(status_code=403, detail="No puede programar turnos para mascotas de otros dueños")

    return crud.create_turno(db=db, turno=turno)

@router.get("/proximos", response_model=List[schemas.TurnoResponse])
def listar_turnos_proximos(
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN":
        my_pets = db.query(models.Mascota).filter(models.Mascota.dueno_cedula == current_user.dueno_cedula).all()
        my_pet_ids = [p.id for p in my_pets]
        if not my_pet_ids:
            return []
        now = datetime.now()
        return db.query(models.Turno).filter(
            models.Turno.mascota_id.in_(my_pet_ids),
            models.Turno.fecha >= now
        ).order_by(models.Turno.fecha.asc()).all()
    return crud.get_turnos_proximos(db)

@router.get("/por-fecha", response_model=List[schemas.TurnoResponse])
def listar_turnos_por_fecha(
    fecha: date,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN":
        my_pets = db.query(models.Mascota).filter(models.Mascota.dueno_cedula == current_user.dueno_cedula).all()
        my_pet_ids = [p.id for p in my_pets]
        if not my_pet_ids:
            return []
        return crud.get_turnos_por_fecha(db, fecha=fecha, mascota_ids=my_pet_ids)
    return crud.get_turnos_por_fecha(db, fecha=fecha)

@router.get("/hoy", response_model=List[schemas.TurnoResponse])
def listar_turnos_hoy(
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN":
        my_pets = db.query(models.Mascota).filter(models.Mascota.dueno_cedula == current_user.dueno_cedula).all()
        my_pet_ids = [p.id for p in my_pets]
        if not my_pet_ids:
            return []
        return crud.get_turnos_hoy(db, mascota_ids=my_pet_ids)
    return crud.get_turnos_hoy(db)

@router.get("/{id}", response_model=schemas.TurnoResponse)
def obtener_turno(
    id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    db_turno = crud.get_turno(db, id=id)
    if not db_turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    if current_user.rol != "ADMIN":
        if not db_turno.mascota or db_turno.mascota.dueno_cedula != current_user.dueno_cedula:
            raise HTTPException(status_code=403, detail="No autorizado a ver este turno")
    return db_turno

@router.put("/{id}", response_model=schemas.TurnoResponse)
def actualizar_turno(
    id: int,
    turno: schemas.TurnoUpdate,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    db_turno = crud.get_turno(db, id=id)
    if not db_turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    if current_user.rol != "ADMIN":
        if not db_turno.mascota or db_turno.mascota.dueno_cedula != current_user.dueno_cedula:
            raise HTTPException(status_code=403, detail="No autorizado a actualizar este turno")
        
        pet_id = turno.mascota_id if turno.mascota_id is not None else turno.mascotaId
        if pet_id is not None:
            db_mascota = crud.get_mascota(db, id=pet_id)
            if not db_mascota or db_mascota.dueno_cedula != current_user.dueno_cedula:
                raise HTTPException(status_code=403, detail="La nueva mascota no pertenece al usuario")

    pet_id = turno.mascota_id if turno.mascota_id is not None else turno.mascotaId
    if pet_id is not None:
        db_mascota = crud.get_mascota(db, id=pet_id)
        if not db_mascota:
            raise HTTPException(status_code=400, detail="La mascota especificada no existe")

    db_turno = crud.update_turno(db, id=id, turno=turno)
    return db_turno

@router.delete("/{id}")
def eliminar_turno(
    id: int,
    db: Session = Depends(database.get_db),
    admin = Depends(require_role("ADMIN"))
):
    success = crud.delete_turno(db, id=id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Turno no encontrado"
        )

    return {
        "message": "Turno eliminado correctamente"
    }
