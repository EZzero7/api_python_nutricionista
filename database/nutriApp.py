from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, JSON, Float, TIMESTAMP, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .database import Base


class Nutricionista(Base):
    __tablename__ = "nutricionista"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hash_password = Column(String)
    apellido = Column(String, nullable=False)
    is_active = Column(Boolean)


class Paciente(Base):
    __tablename__ = "paciente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    sexo = Column(String, nullable=False)
    email = Column(String, nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    actividad_fisica = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    fecha_utl_actualizacion = Column(TIMESTAMP, nullable=False)
    fecha_inicio = Column(TIMESTAMP, nullable=False)
    nutricionista_id = Column(Integer, ForeignKey('nutricionista.id'), nullable=False)
    turno_id = Column(Integer, ForeignKey('turno.id'), nullable=False)
    dieta_id = Column(Integer, ForeignKey('dieta.id'), nullable=False)
    ficha_medica = Column(Integer, ForeignKey('fichaMedica.id'), nullable=False)

    nutricionista = relationship("Nutricionista")
    turno = relationship("Turno")
    dieta = relationship("Dieta")
    fichaMedica = relationship("FichaMedica",foreign_keys=[ficha_medica])


class Turno(Base):
    __tablename__ = 'turno'

    id = Column(Integer, primary_key=True)
    nutricionista_id = Column(Integer, ForeignKey('nutricionista.id'), nullable=False)
    fecha_hora = Column(TIMESTAMP, nullable=False)
    estado = Column(Integer, nullable=False)
    paciente = Column(String, nullable=False)


class Dieta(Base):
    __tablename__ = "dieta"

    id = Column(Integer, primary_key=True)
    nutricionista_id = Column(Integer, ForeignKey('nutricionista.id'), nullable=False)
    detalles = Column(JSON, nullable=False)

    nutricionista = relationship("Nutricionista")


class FichaMedica(Base):
    __tablename__ = "fichaMedica"

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id'), nullable=False)
    dato_medico = Column(JSON, nullable=False)
    detalles = Column(String)
    fecha = Column(TIMESTAMP, nullable=False)