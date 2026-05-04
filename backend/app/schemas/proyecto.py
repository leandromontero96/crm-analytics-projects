from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from app.models.proyecto import EstadoProyectoEnum, TipoProyectoEnum


class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_proyecto: TipoProyectoEnum
    estado: EstadoProyectoEnum = EstadoProyectoEnum.PROPUESTA
    fecha_inicio: Optional[date] = None
    fecha_fin_estimada: Optional[date] = None
    fecha_fin_real: Optional[date] = None
    presupuesto: Optional[float] = None
    costo_actual: float = 0.0
    cliente_id: int


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_proyecto: Optional[TipoProyectoEnum] = None
    estado: Optional[EstadoProyectoEnum] = None
    fecha_inicio: Optional[date] = None
    fecha_fin_estimada: Optional[date] = None
    fecha_fin_real: Optional[date] = None
    presupuesto: Optional[float] = None
    costo_actual: Optional[float] = None


class ProyectoResponse(ProyectoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
