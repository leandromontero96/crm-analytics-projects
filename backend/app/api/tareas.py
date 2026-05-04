from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.tarea import Tarea
from app.schemas.tarea import TareaCreate, TareaUpdate, TareaResponse

router = APIRouter()


@router.post("/", response_model=TareaResponse, status_code=201)
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    """Crear una nueva tarea"""
    db_tarea = Tarea(**tarea.model_dump())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea


@router.get("/", response_model=List[TareaResponse])
def listar_tareas(
    skip: int = 0,
    limit: int = 100,
    proyecto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de tareas, opcionalmente filtradas por proyecto"""
    query = db.query(Tarea)
    if proyecto_id:
        query = query.filter(Tarea.proyecto_id == proyecto_id)
    tareas = query.offset(skip).limit(limit).all()
    return tareas


@router.get("/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(tarea_id: int, db: Session = Depends(get_db)):
    """Obtener una tarea por ID"""
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea


@router.put("/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(tarea_id: int, tarea: TareaUpdate, db: Session = Depends(get_db)):
    """Actualizar una tarea"""
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    update_data = tarea.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tarea, field, value)

    db.commit()
    db.refresh(db_tarea)
    return db_tarea


@router.delete("/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    """Eliminar una tarea"""
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(db_tarea)
    db.commit()
    return None
