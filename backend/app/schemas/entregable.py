from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from app.models.entregable import TipoEntregableEnum, EstadoEntregableEnum


class EntregableBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo: TipoEntregableEnum
    estado: EstadoEntregableEnum = EstadoEntregableEnum.PENDIENTE
    url_archivo: Optional[str] = None
    fecha_entrega_estimada: Optional[date] = None
    fecha_entrega_real: Optional[date] = None
    proyecto_id: int


class EntregableCreate(EntregableBase):
    pass


class EntregableUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[TipoEntregableEnum] = None
    estado: Optional[EstadoEntregableEnum] = None
    url_archivo: Optional[str] = None
    fecha_entrega_estimada: Optional[date] = None
    fecha_entrega_real: Optional[date] = None


class EntregableResponse(EntregableBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
