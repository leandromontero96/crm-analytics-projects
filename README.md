# CRM Analytics Projects

Sistema de gestión de relaciones con clientes (CRM) especializado en proyectos de análisis de datos, construido con FastAPI, PostgreSQL y Streamlit.

## Descripción del Proyecto

**CRM Analytics Projects** es una aplicación web completa diseñada para gestionar clientes, proyectos de análisis de datos, tareas y entregables. Proporciona una interfaz intuitiva para el seguimiento de proyectos analíticos desde la propuesta hasta la entrega final.

### Características Principales

- **Gestión de Clientes**: Registro completo de clientes con información de contacto, industria y notas
- **Gestión de Proyectos**: Control de proyectos con tipos específicos (ML, BI, ETL, etc.), estados y presupuestos
- **Gestión de Tareas**: Seguimiento de tareas con prioridades, estados y asignaciones
- **Gestión de Entregables**: Control de entregables con tipos (informes, dashboards, modelos, etc.)
- **Dashboard Interactivo**: Visualizaciones y métricas en tiempo real
- **API RESTful**: API completa con documentación automática (Swagger/OpenAPI)

## Arquitectura del Sistema

```
crm-analytics-projects/
├── backend/                  # Backend FastAPI
│   ├── app/
│   │   ├── api/             # Endpoints de la API
│   │   │   ├── clientes.py
│   │   │   ├── proyectos.py
│   │   │   ├── tareas.py
│   │   │   └── entregables.py
│   │   ├── core/            # Configuración y base de datos
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── crud/            # Operaciones CRUD
│   │   ├── models/          # Modelos SQLAlchemy
│   │   │   ├── cliente.py
│   │   │   ├── proyecto.py
│   │   │   ├── tarea.py
│   │   │   ├── entregable.py
│   │   │   └── usuario.py
│   │   ├── schemas/         # Schemas Pydantic
│   │   └── main.py          # Aplicación principal
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Frontend Streamlit
│   ├── app.py               # Dashboard principal
│   ├── requirements.txt
│   └── Dockerfile
├── database/                 # Scripts de base de datos
│   └── init.sql
├── docker-compose.yml        # Orquestación de contenedores
├── .env.example             # Variables de entorno de ejemplo
└── README.md

```

## Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido para Python
- **SQLAlchemy**: ORM para interacción con base de datos
- **Pydantic**: Validación de datos y serialización
- **PostgreSQL**: Base de datos relacional
- **Uvicorn**: Servidor ASGI de alto rendimiento

### Frontend
- **Streamlit**: Framework para crear dashboards interactivos
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación y análisis de datos

### DevOps
- **Docker & Docker Compose**: Containerización
- **Alembic**: Migraciones de base de datos

## Instalación y Configuración

### Requisitos Previos

- Python 3.11+
- PostgreSQL 15+
- Docker y Docker Compose (opcional)

### Opción 1: Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd crm-analytics-projects
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Levantar los servicios con Docker Compose**
```bash
docker-compose up -d
```

4. **Acceder a las aplicaciones**
- API Backend: http://localhost:8000
- Documentación API (Swagger): http://localhost:8000/docs
- Dashboard Streamlit: http://localhost:8501

### Opción 2: Instalación Manual

#### 1. Configurar PostgreSQL

```bash
# Crear base de datos
createdb crm_analytics_db

# O usando psql
psql -U postgres
CREATE DATABASE crm_analytics_db;
CREATE USER crm_user WITH PASSWORD 'crm_password';
GRANT ALL PRIVILEGES ON DATABASE crm_analytics_db TO crm_user;
```

#### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp ../.env.example .env
# Editar .env con tus configuraciones

# Ejecutar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Configurar Frontend

```bash
cd frontend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar Streamlit
streamlit run app.py
```

## Uso del Sistema

### API REST

La API proporciona los siguientes endpoints principales:

#### Clientes
- `POST /api/v1/clientes` - Crear cliente
- `GET /api/v1/clientes` - Listar clientes
- `GET /api/v1/clientes/{id}` - Obtener cliente
- `PUT /api/v1/clientes/{id}` - Actualizar cliente
- `DELETE /api/v1/clientes/{id}` - Eliminar cliente

#### Proyectos
- `POST /api/v1/proyectos` - Crear proyecto
- `GET /api/v1/proyectos` - Listar proyectos
- `GET /api/v1/proyectos/{id}` - Obtener proyecto
- `GET /api/v1/proyectos/cliente/{cliente_id}` - Proyectos por cliente
- `PUT /api/v1/proyectos/{id}` - Actualizar proyecto
- `DELETE /api/v1/proyectos/{id}` - Eliminar proyecto

#### Tareas
- `POST /api/v1/tareas` - Crear tarea
- `GET /api/v1/tareas` - Listar tareas (filtrable por proyecto)
- `GET /api/v1/tareas/{id}` - Obtener tarea
- `PUT /api/v1/tareas/{id}` - Actualizar tarea
- `DELETE /api/v1/tareas/{id}` - Eliminar tarea

#### Entregables
- `POST /api/v1/entregables` - Crear entregable
- `GET /api/v1/entregables` - Listar entregables (filtrable por proyecto)
- `GET /api/v1/entregables/{id}` - Obtener entregable
- `PUT /api/v1/entregables/{id}` - Actualizar entregable
- `DELETE /api/v1/entregables/{id}` - Eliminar entregable

### Dashboard Streamlit

El dashboard incluye las siguientes secciones:

1. **Dashboard Principal**
   - Métricas clave (total de clientes, proyectos activos, tareas pendientes, presupuesto total)
   - Gráficos de distribución de proyectos por estado y tipo
   - Lista de proyectos recientes

2. **Gestión de Clientes**
   - Lista de clientes registrados
   - Formulario para registrar nuevos clientes
   - Opción de eliminar clientes

3. **Gestión de Proyectos**
   - Lista de proyectos con detalles expandibles
   - Formulario para crear nuevos proyectos
   - Información de presupuesto y fechas

4. **Gestión de Tareas**
   - Lista de tareas con filtros por proyecto
   - Estados visuales con código de colores
   - Prioridades y fechas de vencimiento

## Modelos de Datos

### Cliente
- ID, Nombre, Empresa, Email, Teléfono
- Industria, Dirección, Notas
- Timestamps de creación y actualización

### Proyecto
- ID, Nombre, Descripción, Tipo de Proyecto
- Estado, Fechas (inicio, fin estimado, fin real)
- Presupuesto, Costo Actual
- Cliente (FK), Timestamps

### Tarea
- ID, Título, Descripción
- Estado, Prioridad
- Fechas (inicio, vencimiento, completada)
- Proyecto (FK), Asignado a (FK), Timestamps

### Entregable
- ID, Nombre, Descripción, Tipo
- Estado, URL/Path del archivo
- Fechas de entrega
- Proyecto (FK), Timestamps

### Usuario
- ID, Nombre, Email, Contraseña (hash)
- Rol, Estado activo
- Timestamps, Último login

## Ejemplos de Uso

### Crear un Cliente (API)

```bash
curl -X POST "http://localhost:8000/api/v1/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "empresa": "Tech Corp",
    "email": "juan@techcorp.com",
    "telefono": "+1234567890",
    "industria": "tecnologia"
  }'
```

### Crear un Proyecto (API)

```bash
curl -X POST "http://localhost:8000/api/v1/proyectos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Dashboard Ventas ML",
    "descripcion": "Dashboard predictivo para análisis de ventas",
    "tipo_proyecto": "machine_learning",
    "estado": "en_progreso",
    "presupuesto": 50000.00,
    "cliente_id": 1
  }'
```

## Tipos de Proyectos Soportados

- **Exploratorio**: Análisis exploratorio de datos
- **Predictivo**: Modelos predictivos y ML
- **Prescriptivo**: Análisis prescriptivo y optimización
- **Dashboard**: Dashboards de visualización
- **ETL Pipeline**: Pipelines de extracción, transformación y carga
- **Machine Learning**: Proyectos de ML complejos
- **Business Intelligence**: Soluciones de BI

## Estados de Proyectos

- **Propuesta**: Proyecto en fase de propuesta
- **En Progreso**: Proyecto activo
- **En Pausa**: Proyecto pausado temporalmente
- **Completado**: Proyecto finalizado
- **Cancelado**: Proyecto cancelado

## Desarrollo y Contribución

### Ejecutar Tests

```bash
cd backend
pytest
```

### Migraciones de Base de Datos

```bash
cd backend

# Crear migración
alembic revision --autogenerate -m "descripción de cambio"

# Aplicar migraciones
alembic upgrade head
```

## Seguridad

- Las contraseñas se almacenan con hash bcrypt
- Soporte para autenticación JWT (implementación futura)
- CORS configurado para orígenes específicos
- Validación de datos con Pydantic

## Mejoras Futuras

- [ ] Autenticación y autorización completa
- [ ] Sistema de notificaciones por email
- [ ] Exportación de reportes en PDF
- [ ] Integración con servicios de almacenamiento en la nube
- [ ] Gráficos de Gantt para proyectos
- [ ] Sistema de comentarios y actividad
- [ ] API de webhooks
- [ ] Integración con herramientas de ML (MLflow, etc.)

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Soporte

Para reportar bugs o solicitar features, por favor crea un issue en el repositorio.

## Autores

Desarrollado con FastAPI, PostgreSQL y Streamlit.

---

**Última actualización**: 2026
**Versión**: 1.0.0
