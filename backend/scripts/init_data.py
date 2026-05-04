"""
Script para inicializar datos de prueba en la base de datos
Ejecutar: python scripts/init_data.py
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import Cliente, Proyecto, Tarea, Entregable, Usuario
from datetime import date, timedelta

def init_db():
    """Crear todas las tablas"""
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente")

def create_sample_data():
    """Crear datos de prueba"""
    db = SessionLocal()

    try:
        print("\nCreando datos de prueba...")

        # Crear clientes
        clientes = [
            Cliente(
                nombre="María González",
                empresa="TechCorp Solutions",
                email="maria@techcorp.com",
                telefono="+1-555-0101",
                industria="tecnologia",
                direccion="Av. Tecnológica 123, Ciudad",
                notas="Cliente premium interesado en ML"
            ),
            Cliente(
                nombre="Carlos Rodríguez",
                empresa="Finance Analytics Group",
                email="carlos@financegroup.com",
                telefono="+1-555-0102",
                industria="finanzas",
                direccion="Calle Wall Street 456",
                notas="Requiere análisis de riesgo crediticio"
            ),
            Cliente(
                nombre="Ana Martínez",
                empresa="Retail Insights Co",
                email="ana@retailinsights.com",
                telefono="+1-555-0103",
                industria="retail",
                direccion="Av. Comercio 789",
                notas="Análisis de comportamiento de compra"
            )
        ]

        for cliente in clientes:
            db.add(cliente)
        db.commit()
        print(f"✓ {len(clientes)} clientes creados")

        # Refrescar para obtener IDs
        for cliente in clientes:
            db.refresh(cliente)

        # Crear proyectos
        proyectos = [
            Proyecto(
                nombre="Sistema Predictivo de Ventas",
                descripcion="Modelo de ML para predecir ventas trimestrales usando XGBoost y LSTM",
                tipo_proyecto="machine_learning",
                estado="en_progreso",
                fecha_inicio=date.today() - timedelta(days=30),
                fecha_fin_estimada=date.today() + timedelta(days=60),
                presupuesto=85000.00,
                costo_actual=32000.00,
                cliente_id=clientes[0].id
            ),
            Proyecto(
                nombre="Dashboard de Análisis de Riesgo",
                descripcion="Dashboard interactivo en Power BI para análisis de riesgo crediticio",
                tipo_proyecto="dashboard",
                estado="propuesta",
                fecha_inicio=date.today() + timedelta(days=15),
                fecha_fin_estimada=date.today() + timedelta(days=75),
                presupuesto=45000.00,
                costo_actual=0.00,
                cliente_id=clientes[1].id
            ),
            Proyecto(
                nombre="ETL Pipeline para Data Warehouse",
                descripcion="Pipeline automatizado para integrar datos de múltiples fuentes",
                tipo_proyecto="etl_pipeline",
                estado="en_progreso",
                fecha_inicio=date.today() - timedelta(days=45),
                fecha_fin_estimada=date.today() + timedelta(days=15),
                presupuesto=65000.00,
                costo_actual=48000.00,
                cliente_id=clientes[1].id
            ),
            Proyecto(
                nombre="Análisis Exploratorio de Comportamiento de Compra",
                descripcion="EDA completo de patrones de compra de clientes",
                tipo_proyecto="exploratorio",
                estado="completado",
                fecha_inicio=date.today() - timedelta(days=90),
                fecha_fin_estimada=date.today() - timedelta(days=30),
                fecha_fin_real=date.today() - timedelta(days=25),
                presupuesto=25000.00,
                costo_actual=23500.00,
                cliente_id=clientes[2].id
            ),
            Proyecto(
                nombre="Sistema de Recomendación de Productos",
                descripcion="Motor de recomendaciones basado en collaborative filtering",
                tipo_proyecto="machine_learning",
                estado="propuesta",
                presupuesto=95000.00,
                costo_actual=0.00,
                cliente_id=clientes[2].id
            )
        ]

        for proyecto in proyectos:
            db.add(proyecto)
        db.commit()
        print(f"✓ {len(proyectos)} proyectos creados")

        # Refrescar proyectos
        for proyecto in proyectos:
            db.refresh(proyecto)

        # Crear tareas
        tareas = [
            Tarea(
                titulo="Análisis exploratorio de datos",
                descripcion="Realizar EDA completo del dataset de ventas históricas",
                estado="completada",
                prioridad="alta",
                fecha_inicio=date.today() - timedelta(days=28),
                fecha_vencimiento=date.today() - timedelta(days=21),
                fecha_completada=date.today() - timedelta(days=20),
                proyecto_id=proyectos[0].id
            ),
            Tarea(
                titulo="Ingeniería de características",
                descripcion="Crear features relevantes para el modelo predictivo",
                estado="en_progreso",
                prioridad="alta",
                fecha_inicio=date.today() - timedelta(days=14),
                fecha_vencimiento=date.today() + timedelta(days=7),
                proyecto_id=proyectos[0].id
            ),
            Tarea(
                titulo="Entrenamiento de modelo XGBoost",
                descripcion="Entrenar y optimizar modelo XGBoost con validación cruzada",
                estado="pendiente",
                prioridad="media",
                fecha_vencimiento=date.today() + timedelta(days=21),
                proyecto_id=proyectos[0].id
            ),
            Tarea(
                titulo="Diseño de arquitectura ETL",
                descripcion="Diseñar arquitectura del pipeline de datos",
                estado="completada",
                prioridad="urgente",
                fecha_inicio=date.today() - timedelta(days=42),
                fecha_vencimiento=date.today() - timedelta(days=35),
                fecha_completada=date.today() - timedelta(days=36),
                proyecto_id=proyectos[2].id
            ),
            Tarea(
                titulo="Implementación de conectores de datos",
                descripcion="Desarrollar conectores para APIs y bases de datos fuente",
                estado="en_progreso",
                prioridad="alta",
                fecha_inicio=date.today() - timedelta(days=20),
                fecha_vencimiento=date.today() + timedelta(days=10),
                proyecto_id=proyectos[2].id
            ),
            Tarea(
                titulo="Reunión de kick-off con cliente",
                descripcion="Presentación del proyecto y definición de alcance",
                estado="pendiente",
                prioridad="urgente",
                fecha_vencimiento=date.today() + timedelta(days=3),
                proyecto_id=proyectos[1].id
            )
        ]

        for tarea in tareas:
            db.add(tarea)
        db.commit()
        print(f"✓ {len(tareas)} tareas creadas")

        # Crear entregables
        entregables = [
            Entregable(
                nombre="Informe de Análisis Exploratorio",
                descripcion="Documento PDF con hallazgos del EDA y visualizaciones",
                tipo="informe",
                estado="entregado",
                fecha_entrega_estimada=date.today() - timedelta(days=20),
                fecha_entrega_real=date.today() - timedelta(days=19),
                proyecto_id=proyectos[0].id
            ),
            Entregable(
                nombre="Modelo Predictivo XGBoost",
                descripcion="Modelo entrenado en formato pickle con documentación",
                tipo="modelo",
                estado="en_desarrollo",
                fecha_entrega_estimada=date.today() + timedelta(days=30),
                proyecto_id=proyectos[0].id
            ),
            Entregable(
                nombre="Dashboard Interactivo",
                descripcion="Dashboard en Streamlit para visualización de predicciones",
                tipo="dashboard",
                estado="pendiente",
                fecha_entrega_estimada=date.today() + timedelta(days=55),
                proyecto_id=proyectos[0].id
            ),
            Entregable(
                nombre="Documentación Técnica del Pipeline",
                descripcion="Documentación completa de arquitectura y configuración",
                tipo="documentacion",
                estado="en_desarrollo",
                fecha_entrega_estimada=date.today() + timedelta(days=10),
                proyecto_id=proyectos[2].id
            ),
            Entregable(
                nombre="Código Fuente del ETL",
                descripcion="Repositorio Git con código fuente y tests",
                tipo="codigo",
                estado="en_desarrollo",
                fecha_entrega_estimada=date.today() + timedelta(days=12),
                proyecto_id=proyectos[2].id
            ),
            Entregable(
                nombre="Presentación de Resultados",
                descripcion="Presentación PowerPoint con insights del análisis",
                tipo="presentacion",
                estado="aprobado",
                fecha_entrega_estimada=date.today() - timedelta(days=30),
                fecha_entrega_real=date.today() - timedelta(days=25),
                proyecto_id=proyectos[3].id
            )
        ]

        for entregable in entregables:
            db.add(entregable)
        db.commit()
        print(f"✓ {len(entregables)} entregables creados")

        print("\n✓ Datos de prueba creados exitosamente!")
        print(f"\nResumen:")
        print(f"  - {len(clientes)} clientes")
        print(f"  - {len(proyectos)} proyectos")
        print(f"  - {len(tareas)} tareas")
        print(f"  - {len(entregables)} entregables")

    except Exception as e:
        print(f"\n✗ Error al crear datos: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Función principal"""
    print("=" * 60)
    print("CRM Analytics Projects - Inicialización de Base de Datos")
    print("=" * 60)

    init_db()
    create_sample_data()

    print("\n" + "=" * 60)
    print("¡Proceso completado!")
    print("Puedes acceder a la API en: http://localhost:8000")
    print("Documentación en: http://localhost:8000/docs")
    print("=" * 60)

if __name__ == "__main__":
    main()
