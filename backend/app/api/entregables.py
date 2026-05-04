from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.entregable import Entregable
from app.schemas.entregable import EntregableCreate, EntregableUpdate, EntregableResponse

router = APIRouter()


@router.post("/", response_model=EntregableResponse, status_code=201)
def crear_entregable(entregable: EntregableCreate, db: Session = Depends(get_db)):
    """Crear un nuevo entregable"""
    db_entregable = Entregable(**entregable.model_dump())
    db.add(db_entregable)
    db.commit()
    db.refresh(db_entregable)
    return db_entregable


@router.get("/", response_model=List[EntregableResponse])
def listar_entregables(
    skip: int = 0,
    limit: int = 100,
    proyecto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de entregables, opcionalmente filtrados por proyecto"""
    query = db.query(Entregable)
    if proyecto_id:
        query = query.filter(Entregable.proyecto_id == proyecto_id)
    entregables = query.offset(skip).limit(limit).all()
    return entregables


@router.get("/{entregable_id}", response_model=EntregableResponse)
def obtener_entregable(entregable_id: int, db: Session = Depends(get_db)):
    """Obtener un entregable por ID"""
    db_entregable = db.query(Entregable).filter(Entregable.id == entregable_id).first()
    if db_entregable is None:
        raise HTTPException(status_code=404, detail="Entregable no encontrado")
    return db_entregable


@router.put("/{entregable_id}", response_model=EntregableResponse)
def actualizar_entregable(entregable_id: int, entregable: EntregableUpdate, db: Session = Depends(get_db)):
    """Actualizar un entregable"""
    db_entregable = db.query(Entregable).filter(Entregable.id == entregable_id).first()
    if db_entregable is None:
        raise HTTPException(status_code=404, detail="Entregable no encontrado")

    update_data = entregable.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entregable, field, value)

    db.commit()
    db.refresh(db_entregable)
    return db_entregable


@router.delete("/{entregable_id}", status_code=204)
def eliminar_entregable(entregable_id: int, db: Session = Depends(get_db)):
    """Eliminar un entregable"""
    db_entregable = db.query(Entregable).filter(Entregable.id == entregable_id).first()
    if db_entregable is None:
        raise HTTPException(status_code=404, detail="Entregable no encontrado")

    db.delete(db_entregable)
    db.commit()
    return None
