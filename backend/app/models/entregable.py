from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class TipoEntregableEnum(str, enum.Enum):
    INFORME = "informe"
    DASHBOARD = "dashboard"
    MODELO = "modelo"
    DATASET = "dataset"
    DOCUMENTACION = "documentacion"
    CODIGO = "codigo"
    PRESENTACION = "presentacion"


class EstadoEntregableEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_DESARROLLO = "en_desarrollo"
    ENTREGADO = "entregado"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class Entregable(Base):
    __tablename__ = "entregables"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    tipo = Column(Enum(TipoEntregableEnum), nullable=False)
    estado = Column(Enum(EstadoEntregableEnum), default=EstadoEntregableEnum.PENDIENTE)

    # URLs/Paths
    url_archivo = Column(String(500))

    # Fechas
    fecha_entrega_estimada = Column(Date)
    fecha_entrega_real = Column(Date)

    # Foreign Keys
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)

    # Timestamps
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    proyecto = relationship("Proyecto", back_populates="entregables")

    def __repr__(self):
        return f"<Entregable(id={self.id}, nombre={self.nombre}, estado={self.estado})>"
