from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.cliente import IndustriaEnum


class ClienteBase(BaseModel):
    nombre: str
    empresa: str
    email: EmailStr
    telefono: Optional[str] = None
    industria: IndustriaEnum = IndustriaEnum.OTROS
    direccion: Optional[str] = None
    notas: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    empresa: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    industria: Optional[IndustriaEnum] = None
    direccion: Optional[str] = None
    notas: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
