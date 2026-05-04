# Documentación de la API - CRM Analytics Projects

## Información General

- **Base URL**: `http://localhost:8000/api/v1`
- **Formato de respuesta**: JSON
- **Autenticación**: No implementada en v1.0 (JWT en versión futura)

## Endpoints

### Clientes

#### Crear Cliente
```http
POST /clientes
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "empresa": "Tech Corp",
  "email": "juan@techcorp.com",
  "telefono": "+1234567890",
  "industria": "tecnologia",
  "direccion": "Calle Principal 123",
  "notas": "Cliente potencial para proyecto de ML"
}
```

**Respuesta (201 Created)**:
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "empresa": "Tech Corp",
  "email": "juan@techcorp.com",
  "telefono": "+1234567890",
  "industria": "tecnologia",
  "direccion": "Calle Principal 123",
  "notas": "Cliente potencial para proyecto de ML",
  "fecha_creacion": "2026-05-04T10:30:00",
  "fecha_actualizacion": "2026-05-04T10:30:00"
}
```

#### Listar Clientes
```http
GET /clientes?skip=0&limit=100
```

#### Obtener Cliente por ID
```http
GET /clientes/{cliente_id}
```

#### Actualizar Cliente
```http
PUT /clientes/{cliente_id}
Content-Type: application/json

{
  "telefono": "+0987654321",
  "notas": "Actualización de contacto"
}
```

#### Eliminar Cliente
```http
DELETE /clientes/{cliente_id}
```

### Proyectos

#### Crear Proyecto
```http
POST /proyectos
Content-Type: application/json

{
  "nombre": "Dashboard Predictivo de Ventas",
  "descripcion": "Implementación de ML para predicción de ventas",
  "tipo_proyecto": "machine_learning",
  "estado": "propuesta",
  "fecha_inicio": "2026-05-15",
  "fecha_fin_estimada": "2026-08-15",
  "presupuesto": 75000.00,
  "costo_actual": 0.00,
  "cliente_id": 1
}
```

**Tipos de Proyecto**:
- `exploratorio`
- `predictivo`
- `prescriptivo`
- `dashboard`
- `etl_pipeline`
- `machine_learning`
- `business_intelligence`

**Estados de Proyecto**:
- `propuesta`
- `en_progreso`
- `en_pausa`
- `completado`
- `cancelado`

#### Listar Proyectos
```http
GET /proyectos?skip=0&limit=100
```

#### Listar Proyectos por Cliente
```http
GET /proyectos/cliente/{cliente_id}
```

#### Obtener Proyecto por ID
```http
GET /proyectos/{proyecto_id}
```

#### Actualizar Proyecto
```http
PUT /proyectos/{proyecto_id}
Content-Type: application/json

{
  "estado": "en_progreso",
  "costo_actual": 15000.00
}
```

#### Eliminar Proyecto
```http
DELETE /proyectos/{proyecto_id}
```

### Tareas

#### Crear Tarea
```http
POST /tareas
Content-Type: application/json

{
  "titulo": "Análisis exploratorio de datos",
  "descripcion": "Realizar EDA completo del dataset de ventas",
  "estado": "pendiente",
  "prioridad": "alta",
  "fecha_inicio": "2026-05-16",
  "fecha_vencimiento": "2026-05-23",
  "proyecto_id": 1,
  "asignado_a_id": null
}
```

**Estados de Tarea**:
- `pendiente`
- `en_progreso`
- `revision`
- `completada`
- `bloqueada`

**Prioridades**:
- `baja`
- `media`
- `alta`
- `urgente`

#### Listar Tareas
```http
GET /tareas?skip=0&limit=100&proyecto_id=1
```

#### Obtener Tarea por ID
```http
GET /tareas/{tarea_id}
```

#### Actualizar Tarea
```http
PUT /tareas/{tarea_id}
Content-Type: application/json

{
  "estado": "completada",
  "fecha_completada": "2026-05-22"
}
```

#### Eliminar Tarea
```http
DELETE /tareas/{tarea_id}
```

### Entregables

#### Crear Entregable
```http
POST /entregables
Content-Type: application/json

{
  "nombre": "Informe de Análisis Exploratorio",
  "descripcion": "Documento con hallazgos del EDA",
  "tipo": "informe",
  "estado": "pendiente",
  "url_archivo": "https://storage.example.com/reports/eda_report.pdf",
  "fecha_entrega_estimada": "2026-05-30",
  "proyecto_id": 1
}
```

**Tipos de Entregable**:
- `informe`
- `dashboard`
- `modelo`
- `dataset`
- `documentacion`
- `codigo`
- `presentacion`

**Estados de Entregable**:
- `pendiente`
- `en_desarrollo`
- `entregado`
- `aprobado`
- `rechazado`

#### Listar Entregables
```http
GET /entregables?skip=0&limit=100&proyecto_id=1
```

#### Obtener Entregable por ID
```http
GET /entregables/{entregable_id}
```

#### Actualizar Entregable
```http
PUT /entregables/{entregable_id}
Content-Type: application/json

{
  "estado": "entregado",
  "fecha_entrega_real": "2026-05-29"
}
```

#### Eliminar Entregable
```http
DELETE /entregables/{entregable_id}
```

## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Eliminación exitosa
- `400 Bad Request`: Error en los datos enviados
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Error de validación
- `500 Internal Server Error`: Error del servidor

## Ejemplos con Python

### Usando requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Crear cliente
cliente_data = {
    "nombre": "María García",
    "empresa": "Data Solutions",
    "email": "maria@datasolutions.com",
    "industria": "tecnologia"
}

response = requests.post(f"{BASE_URL}/clientes", json=cliente_data)
cliente = response.json()
print(f"Cliente creado con ID: {cliente['id']}")

# Listar proyectos
response = requests.get(f"{BASE_URL}/proyectos")
proyectos = response.json()
print(f"Total de proyectos: {len(proyectos)}")

# Actualizar proyecto
proyecto_update = {"estado": "completado"}
response = requests.put(
    f"{BASE_URL}/proyectos/1",
    json=proyecto_update
)
```

## Notas Importantes

1. Todas las fechas deben estar en formato ISO 8601: `YYYY-MM-DD`
2. Los timestamps se devuelven en formato ISO 8601 con timezone UTC
3. Los campos opcionales pueden omitirse en las solicitudes POST/PUT
4. Las operaciones DELETE no devuelven contenido (204 No Content)
5. La paginación se controla con los parámetros `skip` y `limit`

## Documentación Interactiva

Para explorar la API de forma interactiva, visita:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
