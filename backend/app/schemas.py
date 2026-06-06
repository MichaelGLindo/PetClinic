from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Dueno Schemas
class DuenoBase(BaseModel):
    cedula: str
    nombre: Optional[str] = None
    telefono: Optional[str] = None

class DuenoCreate(DuenoBase):
    pass

class DuenoResponse(DuenoBase):
    model_config = ConfigDict(from_attributes=True)


# Mascota Schemas
class MascotaCreate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    edad: Optional[int] = None
    # Flexible fields to support different ways the client might send the owner reference
    cedulaDueno: Optional[str] = None
    dueno_cedula: Optional[str] = None
    dueno: Optional[DuenoResponse] = None

class MascotaResponse(BaseModel):
    id: int
    nombre: Optional[str] = None
    especie: Optional[str] = None
    edad: Optional[int] = None
    dueno: Optional[DuenoResponse] = None

    model_config = ConfigDict(from_attributes=True)


# Turno Schemas
class TurnoCreate(BaseModel):
    fecha: Optional[datetime] = None
    motivo: Optional[str] = None
    # Flexible fields to support different ways the client might send the pet reference
    mascotaId: Optional[int] = None
    mascota_id: Optional[int] = None
    mascota: Optional[BaseModel] = None # e.g., if passed as an object containing id

class TurnoResponse(BaseModel):
    id: int
    fecha: Optional[datetime] = None
    motivo: Optional[str] = None
    mascota: Optional[MascotaResponse] = None

    model_config = ConfigDict(from_attributes=True)
