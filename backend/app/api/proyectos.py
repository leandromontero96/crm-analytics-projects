from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoResponse
from app.crud import proyecto_crud

router = APIRouter()


@router.post("/", response_model=ProyectoResponse, status_code=201)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo proyecto"""
    return proyecto_crud.create_proyecto(db=db, proyecto=proyecto)


@router.get("/", response_model=List[ProyectoResponse])
def listar_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de proyectos"""
    proyectos = proyecto_crud.get_proyectos(db, skip=skip, limit=limit)
    return proyectos


@router.get("/cliente/{cliente_id}", response_model=List[ProyectoResponse])
def listar_proyectos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener proyectos de un cliente específico"""
    proyectos = proyecto_crud.get_proyectos_by_cliente(db, cliente_id=cliente_id)
    return proyectos


@router.get("/{proyecto_id}", response_model=ProyectoResponse)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    """Obtener un proyecto por ID"""
    db_proyecto = proyecto_crud.get_proyecto(db, proyecto_id=proyecto_id)
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto


@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto(proyecto_id: int, proyecto: ProyectoUpdate, db: Session = Depends(get_db)):
    """Actualizar un proyecto"""
    db_proyecto = proyecto_crud.update_proyecto(db, proyecto_id=proyecto_id, proyecto=proyecto)
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto


@router.delete("/{proyecto_id}", status_code=204)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    """Eliminar un proyecto"""
    success = proyecto_crud.delete_proyecto(db, proyecto_id=proyecto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return None
