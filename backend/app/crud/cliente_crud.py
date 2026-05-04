from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def get_cliente(db: Session, cliente_id: int) -> Optional[Cliente]:
    """Obtener un cliente por ID"""
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def get_clientes(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
    """Obtener lista de clientes"""
    return db.query(Cliente).offset(skip).limit(limit).all()


def get_cliente_by_email(db: Session, email: str) -> Optional[Cliente]:
    """Obtener cliente por email"""
    return db.query(Cliente).filter(Cliente.email == email).first()


def create_cliente(db: Session, cliente: ClienteCreate) -> Cliente:
    """Crear nuevo cliente"""
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def update_cliente(db: Session, cliente_id: int, cliente: ClienteUpdate) -> Optional[Cliente]:
    """Actualizar cliente"""
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        update_data = cliente.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, cliente_id: int) -> bool:
    """Eliminar cliente"""
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return True
    return False
