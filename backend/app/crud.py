from sqlalchemy.orm import Session
from datetime import datetime, date, time
from app import models, schemas

# Dueno CRUD
def get_duenos(db: Session):
    return db.query(models.Dueno).all()

def get_dueno(db: Session, cedula: str):
    return db.query(models.Dueno).filter(models.Dueno.cedula == cedula).first()

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

def update_dueno(db: Session, cedula: str, dueno: schemas.DuenoUpdate):
    db_dueno = get_dueno(db, cedula)
    if not db_dueno:
        return None
    if dueno.nombre is not None:
        db_dueno.nombre = dueno.nombre
    if dueno.telefono is not None:
        db_dueno.telefono = dueno.telefono
    db.commit()
    db.refresh(db_dueno)
    return db_dueno

def delete_dueno(db: Session, cedula: str):
    db_dueno = get_dueno(db, cedula)
    if not db_dueno:
        return False
    db.delete(db_dueno)
    db.commit()
    return True


# Mascota CRUD
def get_mascotas(db: Session, dueno_cedula: str = None):
    query = db.query(models.Mascota)
    if dueno_cedula:
        query = query.filter(models.Mascota.dueno_cedula == dueno_cedula)
    return query.all()

def get_mascota(db: Session, id: int):
    return db.query(models.Mascota).filter(models.Mascota.id == id).first()

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

def update_mascota(db: Session, id: int, mascota: schemas.MascotaUpdate):
    db_mascota = get_mascota(db, id)
    if not db_mascota:
        return None
    if mascota.nombre is not None:
        db_mascota.nombre = mascota.nombre
    if mascota.especie is not None:
        db_mascota.especie = mascota.especie
    if mascota.edad is not None:
        db_mascota.edad = mascota.edad

    # Resolve owner's cedula from flexible inputs
    owner_cedula = None
    if mascota.dueno_cedula is not None:
        owner_cedula = mascota.dueno_cedula
    elif mascota.cedulaDueno is not None:
        owner_cedula = mascota.cedulaDueno
    elif mascota.dueno and hasattr(mascota.dueno, 'cedula'):
        owner_cedula = mascota.dueno.cedula

    if owner_cedula is not None:
        db_mascota.dueno_cedula = owner_cedula

    db.commit()
    db.refresh(db_mascota)
    return db_mascota

def delete_mascota(db: Session, id: int):
    db_mascota = get_mascota(db, id)
    if not db_mascota:
        return False
    db.delete(db_mascota)
    db.commit()
    return True


# Turno CRUD
def get_turnos(db: Session, mascota_id: int = None):
    query = db.query(models.Turno)
    if mascota_id is not None:
        query = query.filter(models.Turno.mascota_id == mascota_id)
    return query.all()

def get_turno(db: Session, id: int):
    return db.query(models.Turno).filter(models.Turno.id == id).first()

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

def update_turno(db: Session, id: int, turno: schemas.TurnoUpdate):
    db_turno = get_turno(db, id)
    if not db_turno:
        return None
    if turno.fecha is not None:
        db_turno.fecha = turno.fecha
    if turno.motivo is not None:
        db_turno.motivo = turno.motivo

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

    if pet_id is not None:
        db_turno.mascota_id = pet_id

    db.commit()
    db.refresh(db_turno)
    return db_turno

def delete_turno(db: Session, id: int):
    db_turno = get_turno(db, id)
    if not db_turno:
        return False
    db.delete(db_turno)
    db.commit()
    return True

# Dashboard statistics
def get_dashboard_stats(db: Session):
    total_duenos = db.query(models.Dueno).count()
    total_mascotas = db.query(models.Mascota).count()
    total_turnos = db.query(models.Turno).count()

    # Get upcoming turnos for the rest of today
    now = datetime.now()
    end_of_today = datetime.combine(date.today(), time.max)
    proximos_turnos = db.query(models.Turno).filter(
        models.Turno.fecha >= now,
        models.Turno.fecha <= end_of_today
    ).order_by(models.Turno.fecha.asc()).all()

    return {
        "total_duenos": total_duenos,
        "total_mascotas": total_mascotas,
        "total_turnos": total_turnos,
        "proximos_turnos": proximos_turnos,
        
        "totalDuenos": total_duenos,
        "totalMascotas": total_mascotas,
        "totalTurnos": total_turnos,
        "proximosTurnos": proximos_turnos
    }

def get_turnos_proximos(db: Session):
    now = datetime.now()
    return db.query(models.Turno).filter(
        models.Turno.fecha >= now
    ).order_by(models.Turno.fecha.asc()).all()

def get_mascota_max_edad(db: Session):
    from sqlalchemy import func
    max_edad = db.query(func.max(models.Mascota.edad)).scalar()
    if max_edad is None:
        return []
    return db.query(models.Mascota).filter(models.Mascota.edad == max_edad).all()


# HistorialClinico CRUD
def _resolve_mascota_id_historial(historial):
    pet_id = None
    if getattr(historial, 'mascota_id', None) is not None:
        pet_id = historial.mascota_id
    elif getattr(historial, 'mascotaId', None) is not None:
        pet_id = historial.mascotaId
    return pet_id

def get_historiales(db: Session, mascota_id: int = None):
    query = db.query(models.HistorialClinico)
    if mascota_id is not None:
        query = query.filter(models.HistorialClinico.mascota_id == mascota_id)
    return query.order_by(models.HistorialClinico.fecha.desc()).all()

def get_historial(db: Session, id: int):
    return db.query(models.HistorialClinico).filter(models.HistorialClinico.id == id).first()

def create_historial(db: Session, historial: schemas.HistorialClinicoCreate):
    pet_id = _resolve_mascota_id_historial(historial)
    db_historial = models.HistorialClinico(
        fecha=historial.fecha,
        descripcion=historial.descripcion,
        diagnostico=historial.diagnostico,
        mascota_id=pet_id
    )
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial

def update_historial(db: Session, id: int, historial: schemas.HistorialClinicoUpdate):
    db_historial = get_historial(db, id)
    if not db_historial:
        return None
    if historial.fecha is not None:
        db_historial.fecha = historial.fecha
    if historial.descripcion is not None:
        db_historial.descripcion = historial.descripcion
    if historial.diagnostico is not None:
        db_historial.diagnostico = historial.diagnostico

    pet_id = _resolve_mascota_id_historial(historial)
    if pet_id is not None:
        db_historial.mascota_id = pet_id

    db.commit()
    db.refresh(db_historial)
    return db_historial

def delete_historial(db: Session, id: int):
    db_historial = get_historial(db, id)
    if not db_historial:
        return False
    db.delete(db_historial)
    db.commit()
    return True

