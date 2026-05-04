# Guía de Inicio Rápido - CRM Analytics Projects

## Inicio Rápido con Docker (5 minutos)

### Prerrequisitos
- Docker Desktop instalado
- Git (opcional)

### Pasos

1. **Clonar o descargar el proyecto**
```bash
git clone <repository-url>
cd crm-analytics-projects
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
```

3. **Levantar servicios**
```bash
docker-compose up -d
```

4. **Inicializar datos de prueba**
```bash
docker-compose exec backend python scripts/init_data.py
```

5. **Acceder a las aplicaciones**
- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

¡Listo! Ya puedes empezar a usar el CRM.

## Primeros Pasos en el Dashboard

### 1. Ver el Dashboard Principal
- Abre http://localhost:8501
- Verás métricas generales y gráficos

### 2. Gestionar Clientes
- Click en "👥 Clientes" en el sidebar
- Puedes ver la lista de clientes de ejemplo
- Prueba crear un nuevo cliente en la pestaña "➕ Nuevo Cliente"

### 3. Gestionar Proyectos
- Click en "📁 Proyectos"
- Explora los proyectos de ejemplo
- Crea un nuevo proyecto asociado a un cliente

### 4. Ver Tareas
- Click en "✅ Tareas"
- Filtra tareas por proyecto
- Observa los estados con código de colores

## Uso de la API

### Ejemplo 1: Listar todos los clientes
```bash
curl http://localhost:8000/api/v1/clientes
```

### Ejemplo 2: Crear un nuevo proyecto
```bash
curl -X POST http://localhost:8000/api/v1/proyectos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Mi Primer Proyecto",
    "tipo_proyecto": "dashboard",
    "estado": "propuesta",
    "presupuesto": 50000,
    "cliente_id": 1
  }'
```

### Ejemplo 3: Ver documentación interactiva
Visita http://localhost:8000/docs para explorar todos los endpoints disponibles.

## Datos de Prueba Incluidos

El script de inicialización crea:
- **3 clientes** de diferentes industrias (tecnología, finanzas, retail)
- **5 proyectos** en diferentes estados (propuesta, en progreso, completado)
- **6 tareas** con diferentes prioridades y estados
- **6 entregables** de varios tipos (informes, dashboards, modelos, etc.)

## Comandos Útiles

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Reiniciar servicios
```bash
docker-compose restart
```

### Detener servicios
```bash
docker-compose down
```

### Limpiar todo (incluye datos)
```bash
docker-compose down -v
```

## Resolución de Problemas

### El backend no inicia
```bash
# Ver logs
docker-compose logs backend

# Reiniciar
docker-compose restart backend
```

### El frontend muestra errores de conexión
- Verifica que el backend esté corriendo: http://localhost:8000/health
- Revisa que la URL de la API esté correcta en `frontend/app.py`

### La base de datos no tiene datos
```bash
# Ejecutar script de inicialización
docker-compose exec backend python scripts/init_data.py
```

## Próximos Pasos

1. **Explorar la API**: Visita http://localhost:8000/docs
2. **Personalizar datos**: Modifica el script `backend/scripts/init_data.py`
3. **Leer documentación completa**: Consulta `README.md`
4. **Ver guía de despliegue**: Consulta `docs/DEPLOYMENT.md`
5. **Explorar código fuente**: Revisa la estructura del proyecto

## Recursos Adicionales

- **README.md**: Documentación completa
- **docs/API_DOCUMENTATION.md**: Guía detallada de la API
- **docs/DEPLOYMENT.md**: Guía de despliegue en producción

## Contacto y Soporte

Si encuentras problemas o tienes preguntas:
1. Revisa la documentación en `README.md`
2. Consulta los logs con `docker-compose logs`
3. Abre un issue en el repositorio

---

¡Disfruta usando CRM Analytics Projects! 🚀
