from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Dueno(Base):
    __tablename__ = "duenos"

    cedula = Column(String(255), primary_key=True, index=True)
    nombre = Column(String(255), nullable=True)
    telefono = Column(String(255), nullable=True)


class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=True)
    especie = Column(String(255), nullable=True)
    edad = Column(Integer, nullable=True)
    dueno_cedula = Column(String(255), ForeignKey("duenos.cedula"), nullable=True)

    dueno = relationship("Dueno", lazy="joined")


class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(DateTime, nullable=True)
    motivo = Column(String(255), nullable=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=True)

    mascota = relationship("Mascota", lazy="joined")


class HistorialClinico(Base):
    __tablename__ = "historiales_clinicos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(DateTime, nullable=True)
    descripcion = Column(String(1000), nullable=True)
    diagnostico = Column(String(500), nullable=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=True)

    mascota = relationship("Mascota", lazy="joined")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)