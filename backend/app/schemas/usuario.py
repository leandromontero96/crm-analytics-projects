from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.usuario import RolEnum


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: RolEnum = RolEnum.ANALISTA
    is_active: bool = True


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[RolEnum] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    ultimo_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
