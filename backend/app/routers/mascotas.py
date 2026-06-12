from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database
from app.auth_dependencies import get_current_user
from app.roles import require_role

router = APIRouter(
    prefix="/api/mascotas",
    tags=["mascotas"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[schemas.MascotaResponse])
def listar_mascotas(
    dueno_cedula: str | None = None,
    cedulaDueno: str | None = None,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN":
        cedula = current_user.dueno_cedula
        if not cedula:
            return []
    else:
        cedula = dueno_cedula or cedulaDueno
    return crud.get_mascotas(db, dueno_cedula=cedula)

@router.post("", response_model=schemas.MascotaResponse)
def guardar_mascota(
    mascota: schemas.MascotaCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN":
        mascota.dueno_cedula = current_user.dueno_cedula
        mascota.cedulaDueno = current_user.dueno_cedula

    owner_cedula = mascota.dueno_cedula or mascota.cedulaDueno
    if not owner_cedula:
        raise HTTPException(status_code=400, detail="Debe especificar un dueño")

    db_dueno = crud.get_dueno(db, cedula=owner_cedula)
    if not db_dueno:
        raise HTTPException(status_code=400, detail="El dueño especificado no existe")

    return crud.create_mascota(db=db, mascota=mascota)

@router.get("/buscar/max", response_model=List[schemas.MascotaResponse])
def obtener_mascota_max_edad(
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    # If client, only search within their own pets
    if current_user.rol != "ADMIN":
        cedula = current_user.dueno_cedula
        if not cedula:
            return []
        all_my_pets = crud.get_mascotas(db, dueno_cedula=cedula)
        if not all_my_pets:
            return []
        max_age = max(p.edad for p in all_my_pets if p.edad is not None)
        return [p for p in all_my_pets if p.edad == max_age]
    return crud.get_mascota_max_edad(db)

@router.get("/{id}", response_model=schemas.MascotaResponse)
def obtener_mascota(
    id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    db_mascota = crud.get_mascota(db, id=id)
    if not db_mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    if current_user.rol != "ADMIN" and (not db_mascota.dueno or db_mascota.dueno.cedula != current_user.dueno_cedula):
        raise HTTPException(status_code=403, detail="No autorizado a ver esta mascota")
    return db_mascota

@router.put("/{id}", response_model=schemas.MascotaResponse)
def actualizar_mascota(
    id: int,
    mascota: schemas.MascotaUpdate,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    db_mascota = crud.get_mascota(db, id=id)
    if not db_mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    if current_user.rol != "ADMIN":
        if not db_mascota.dueno or db_mascota.dueno.cedula != current_user.dueno_cedula:
            raise HTTPException(status_code=403, detail="No autorizado a actualizar esta mascota")
        mascota.dueno_cedula = current_user.dueno_cedula
        mascota.cedulaDueno = current_user.dueno_cedula

    owner_cedula = mascota.dueno_cedula or mascota.cedulaDueno
    if owner_cedula:
        db_dueno = crud.get_dueno(db, cedula=owner_cedula)
        if not db_dueno:
            raise HTTPException(status_code=400, detail="El dueño especificado no existe")

    db_mascota = crud.update_mascota(db, id=id, mascota=mascota)
    return db_mascota

@router.delete("/{id}")
def eliminar_mascota(
    id: int,
    db: Session = Depends(database.get_db),
    admin = Depends(require_role("ADMIN"))
):
    success = crud.delete_mascota(db, id=id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Mascota no encontrada"
        )

    return {
        "message": "Mascota eliminada correctamente"
    }