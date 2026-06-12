from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database
from app.auth_dependencies import get_current_user
from app.roles import require_role
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/api/duenos",
    tags=["duenos"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[schemas.DuenoResponse])
def listar_duenos(
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN":
        if current_user.dueno_cedula:
            db_dueno = crud.get_dueno(db, cedula=current_user.dueno_cedula)
            return [db_dueno] if db_dueno else []
        return []
    return crud.get_duenos(db)

@router.post("", response_model=schemas.DuenoResponse)
def guardar_dueno(
    dueno: schemas.DuenoCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN":
        raise HTTPException(status_code=403, detail="No autorizado para registrar dueños de forma directa")
    db_dueno = crud.get_dueno(db, cedula=dueno.cedula)
    if db_dueno:
        raise HTTPException(status_code=400, detail="Ya existe un dueño con esa cédula")
    return crud.create_dueno(db=db, dueno=dueno)

@router.get("/{cedula}", response_model=schemas.DuenoResponse)
def obtener_dueno(
    cedula: str,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN" and current_user.dueno_cedula != cedula:
        raise HTTPException(status_code=403, detail="No autorizado a ver este dueño")
    db_dueno = crud.get_dueno(db, cedula=cedula)
    if not db_dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    return db_dueno

@router.put("/{cedula}", response_model=schemas.DuenoResponse)
def actualizar_dueno(
    cedula: str,
    dueno: schemas.DuenoUpdate,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "ADMIN" and current_user.dueno_cedula != cedula:
        raise HTTPException(status_code=403, detail="No autorizado a modificar este dueño")
    db_dueno = crud.update_dueno(db, cedula=cedula, dueno=dueno)
    if not db_dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    return db_dueno

@router.delete("/{cedula}")
def eliminar_dueno(
    cedula: str,
    db: Session = Depends(database.get_db),
    user=Depends(require_role("ADMIN"))
):
    success = crud.delete_dueno(db, cedula=cedula)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Dueño no encontrado"
        )

    return {
        "message": "Dueño eliminado correctamente"
    }
