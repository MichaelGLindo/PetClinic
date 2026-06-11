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

class DuenoUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None

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

class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    edad: Optional[int] = None
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

class TurnoUpdate(BaseModel):
    fecha: Optional[datetime] = None
    motivo: Optional[str] = None
    mascotaId: Optional[int] = None
    mascota_id: Optional[int] = None
    mascota: Optional[BaseModel] = None

class TurnoResponse(BaseModel):
    id: int
    fecha: Optional[datetime] = None
    motivo: Optional[str] = None
    mascota: Optional[MascotaResponse] = None

    model_config = ConfigDict(from_attributes=True)


class DashboardStatsResponse(BaseModel):
    total_duenos: int
    total_mascotas: int
    total_turnos: int
    proximos_turnos: list[TurnoResponse]
    
    # Frontend camelCase compatibility
    totalDuenos: int
    totalMascotas: int
    totalTurnos: int
    proximosTurnos: list[TurnoResponse]


# HistorialClinico Schemas
class HistorialClinicoCreate(BaseModel):
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    diagnostico: Optional[str] = None
    mascotaId: Optional[int] = None
    mascota_id: Optional[int] = None

class HistorialClinicoUpdate(BaseModel):
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    diagnostico: Optional[str] = None
    mascotaId: Optional[int] = None
    mascota_id: Optional[int] = None

class HistorialClinicoResponse(BaseModel):
    id: int
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    diagnostico: Optional[str] = None
    mascota: Optional[MascotaResponse] = None

    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(BaseModel):
    username: str
    password: str
    rol: str 


class UsuarioLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str