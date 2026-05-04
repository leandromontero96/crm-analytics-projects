from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class EstadoTareaEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    REVISIÓN = "revision"
    COMPLETADA = "completada"
    BLOQUEADA = "bloqueada"


class PrioridadEnum(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    estado = Column(Enum(EstadoTareaEnum), default=EstadoTareaEnum.PENDIENTE)
    prioridad = Column(Enum(PrioridadEnum), default=PrioridadEnum.MEDIA)

    # Fechas
    fecha_inicio = Column(Date)
    fecha_vencimiento = Column(Date)
    fecha_completada = Column(Date)

    # Foreign Keys
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)
    asignado_a_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))

    # Timestamps
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    proyecto = relationship("Proyecto", back_populates="tareas")
    asignado_a = relationship("Usuario", back_populates="tareas")

    def __repr__(self):
        return f"<Tarea(id={self.id}, titulo={self.titulo}, estado={self.estado})>"
