from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate


def get_proyecto(db: Session, proyecto_id: int) -> Optional[Proyecto]:
    """Obtener un proyecto por ID"""
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()


def get_proyectos(db: Session, skip: int = 0, limit: int = 100) -> List[Proyecto]:
    """Obtener lista de proyectos"""
    return db.query(Proyecto).offset(skip).limit(limit).all()


def get_proyectos_by_cliente(db: Session, cliente_id: int) -> List[Proyecto]:
    """Obtener proyectos de un cliente"""
    return db.query(Proyecto).filter(Proyecto.cliente_id == cliente_id).all()


def create_proyecto(db: Session, proyecto: ProyectoCreate) -> Proyecto:
    """Crear nuevo proyecto"""
    db_proyecto = Proyecto(**proyecto.model_dump())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto


def update_proyecto(db: Session, proyecto_id: int, proyecto: ProyectoUpdate) -> Optional[Proyecto]:
    """Actualizar proyecto"""
    db_proyecto = get_proyecto(db, proyecto_id)
    if db_proyecto:
        update_data = proyecto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_proyecto, field, value)
        db.commit()
        db.refresh(db_proyecto)
    return db_proyecto


def delete_proyecto(db: Session, proyecto_id: int) -> bool:
    """Eliminar proyecto"""
    db_proyecto = get_proyecto(db, proyecto_id)
    if db_proyecto:
        db.delete(db_proyecto)
        db.commit()
        return True
    return False
