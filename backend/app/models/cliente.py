from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class IndustriaEnum(str, enum.Enum):
    TECNOLOGIA = "tecnologia"
    FINANZAS = "finanzas"
    RETAIL = "retail"
    SALUD = "salud"
    MANUFACTURA = "manufactura"
    ENERGIA = "energia"
    TELECOMUNICACIONES = "telecomunicaciones"
    OTROS = "otros"


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    empresa = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telefono = Column(String(50))
    industria = Column(Enum(IndustriaEnum), default=IndustriaEnum.OTROS)
    direccion = Column(Text)
    notas = Column(Text)

    # Timestamps
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    proyectos = relationship("Proyecto", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nombre={self.nombre}, empresa={self.empresa})>"
