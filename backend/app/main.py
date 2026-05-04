from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import clientes, proyectos, tareas, entregables

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gestión de CRM de proyectos de análisis de datos"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(clientes.router, prefix=f"{settings.API_V1_STR}/clientes", tags=["Clientes"])
app.include_router(proyectos.router, prefix=f"{settings.API_V1_STR}/proyectos", tags=["Proyectos"])
app.include_router(tareas.router, prefix=f"{settings.API_V1_STR}/tareas", tags=["Tareas"])
app.include_router(entregables.router, prefix=f"{settings.API_V1_STR}/entregables", tags=["Entregables"])


@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "message": "CRM Analytics Projects API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
