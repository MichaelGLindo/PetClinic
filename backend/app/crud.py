from sqlalchemy.orm import Session
from app import models, schemas

# Dueno CRUD
def get_duenos(db: Session):
    return db.query(models.Dueno).all()

def create_dueno(db: Session, dueno: schemas.DuenoCreate):
    db_dueno = models.Dueno(
        cedula=dueno.cedula,
        nombre=dueno.nombre,
        telefono=dueno.telefono
    )
    db.add(db_dueno)
    db.commit()
    db.refresh(db_dueno)
    return db_dueno


# Mascota CRUD
def get_mascotas(db: Session):
    return db.query(models.Mascota).all()

def create_mascota(db: Session, mascota: schemas.MascotaCreate):
    # Resolve the owner's cedula from flexible inputs
    owner_cedula = None
    if mascota.dueno_cedula:
        owner_cedula = mascota.dueno_cedula
    elif mascota.cedulaDueno:
        owner_cedula = mascota.cedulaDueno
    elif mascota.dueno and hasattr(mascota.dueno, 'cedula'):
        owner_cedula = mascota.dueno.cedula

    db_mascota = models.Mascota(
        nombre=mascota.nombre,
        especie=mascota.especie,
        edad=mascota.edad,
        dueno_cedula=owner_cedula
    )
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota


# Turno CRUD
def get_turnos(db: Session):
    return db.query(models.Turno).all()

def create_turno(db: Session, turno: schemas.TurnoCreate):
    # Resolve the pet's ID from flexible inputs
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

    db_turno = models.Turno(
        fecha=turno.fecha,
        motivo=turno.motivo,
        mascota_id=pet_id
    )
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno
