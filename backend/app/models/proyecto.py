from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class EstadoProyectoEnum(str, enum.Enum):
    PROPUESTA = "propuesta"
    EN_PROGRESO = "en_progreso"
    EN_PAUSA = "en_pausa"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class TipoProyectoEnum(str, enum.Enum):
    EXPLORATORIO = "exploratorio"
    PREDICTIVO = "predictivo"
    PRESCRIPTIVO = "prescriptivo"
    DASHBOARD = "dashboard"
    ETL_PIPELINE = "etl_pipeline"
    MACHINE_LEARNING = "machine_learning"
    BUSINESS_INTELLIGENCE = "business_intelligence"


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    descripcion = Column(Text)
    tipo_proyecto = Column(Enum(TipoProyectoEnum), nullable=False)
    estado = Column(Enum(EstadoProyectoEnum), default=EstadoProyectoEnum.PROPUESTA)

    # Fechas
    fecha_inicio = Column(Date)
    fecha_fin_estimada = Column(Date)
    fecha_fin_real = Column(Date)

    # Financiero
    presupuesto = Column(Float)
    costo_actual = Column(Float, default=0.0)

    # Foreign Keys
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)

    # Timestamps
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cliente = relationship("Cliente", back_populates="proyectos")
    tareas = relationship("Tarea", back_populates="proyecto", cascade="all, delete-orphan")
    entregables = relationship("Entregable", back_populates="proyecto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre={self.nombre}, estado={self.estado})>"
