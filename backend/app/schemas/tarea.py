from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from app.models.tarea import EstadoTareaEnum, PrioridadEnum


class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: EstadoTareaEnum = EstadoTareaEnum.PENDIENTE
    prioridad: PrioridadEnum = PrioridadEnum.MEDIA
    fecha_inicio: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    fecha_completada: Optional[date] = None
    proyecto_id: int
    asignado_a_id: Optional[int] = None


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[EstadoTareaEnum] = None
    prioridad: Optional[PrioridadEnum] = None
    fecha_inicio: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    fecha_completada: Optional[date] = None
    asignado_a_id: Optional[int] = None


class TareaResponse(TareaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
