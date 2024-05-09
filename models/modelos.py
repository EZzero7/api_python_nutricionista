from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NutricionistaModel(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellido: str
    email: str
    hash_password: str
    is_active : bool

class Credentials(NutricionistaModel):
    email: str
    hash_password: str

class PacienteModel(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellido: str
    edad: int
    sexo: str
    email: str
    peso: float
    altura: float
    actividad_fisica: int
    is_active: bool
    fecha_utl_actualizacion: datetime
    fecha_inicio: datetime
    nutricionista_id: int
    turno_id: int
    dieta_id: int
    ficha_medica: int

class TurnoModel(BaseModel):
    id: Optional[int] = None
    nutricionista_id: int
    paciente: str
    fecha_hora: datetime
    estado: int

class DietaModel(BaseModel):
    id: Optional[int] = None
    detalles: dict
    nutricionista_id: int


class FichaMedicaModel(BaseModel):
    id: Optional[int] = None
    paciente_id: int
    dato_medico: dict
    detalles: str
    fecha: datetime