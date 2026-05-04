# Guía de Despliegue - CRM Analytics Projects

## Despliegue en Desarrollo

### Usando Docker Compose (Recomendado)

1. **Configurar variables de entorno**
```bash
cp .env.example .env
```

2. **Levantar servicios**
```bash
docker-compose up -d
```

3. **Ver logs**
```bash
docker-compose logs -f
```

4. **Detener servicios**
```bash
docker-compose down
```

## Despliegue en Producción

### Requisitos Previos

- Servidor con Docker y Docker Compose instalados
- Dominio configurado (opcional)
- Certificado SSL (recomendado)

### 1. Configuración de Variables de Entorno

Crear archivo `.env` con valores de producción:

```bash
# Base de datos
POSTGRES_SERVER=postgres
POSTGRES_USER=crm_prod_user
POSTGRES_PASSWORD=STRONG_PASSWORD_HERE
POSTGRES_DB=crm_analytics_prod
POSTGRES_PORT=5432

# Seguridad
SECRET_KEY=GENERATE_STRONG_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

### 2. Configuración de PostgreSQL

Para producción, considera usar PostgreSQL en un servicio gestionado:

- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL
- DigitalOcean Managed Databases

Actualiza `POSTGRES_SERVER` en `.env` con el endpoint del servicio.

### 3. Configuración de Docker Compose para Producción

Crear `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: crm_backend_prod
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: crm_frontend_prod
    command: streamlit run app.py --server.port 8501 --server.address 0.0.0.0
    ports:
      - "8501:8501"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: crm_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

### 4. Configuración de Nginx

Crear `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:8501;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # API Backend
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Streamlit Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support for Streamlit
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### 5. Generar Certificado SSL (Let's Encrypt)

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Generar certificado
sudo certbot --nginx -d yourdomain.com
```

### 6. Desplegar

```bash
# Construir y levantar servicios
docker-compose -f docker-compose.prod.yml up -d --build

# Verificar que los contenedores estén corriendo
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Despliegue en la Nube

### AWS (Amazon Web Services)

#### Opción 1: ECS (Elastic Container Service)

1. Crear repositorios ECR para las imágenes
2. Construir y subir imágenes a ECR
3. Crear Task Definitions
4. Configurar ECS Service con Load Balancer
5. Configurar RDS para PostgreSQL

#### Opción 2: EC2 con Docker

1. Lanzar instancia EC2
2. Instalar Docker y Docker Compose
3. Clonar repositorio y configurar
4. Ejecutar con docker-compose

### Google Cloud Platform

#### Opción 1: Cloud Run

```bash
# Backend
gcloud run deploy crm-backend \
  --source ./backend \
  --platform managed \
  --region us-central1

# Frontend
gcloud run deploy crm-frontend \
  --source ./frontend \
  --platform managed \
  --region us-central1
```

#### Opción 2: GKE (Google Kubernetes Engine)

Crear manifiestos de Kubernetes y desplegar con kubectl.

### DigitalOcean

1. Crear Droplet
2. Instalar Docker y Docker Compose
3. Configurar firewall
4. Desplegar con docker-compose

### Heroku

```bash
# Backend
heroku create crm-analytics-backend
heroku addons:create heroku-postgresql:hobby-dev
git subtree push --prefix backend heroku main

# Frontend (requiere configuración adicional)
```

## Monitoreo y Mantenimiento

### Logs

```bash
# Ver logs del backend
docker-compose logs -f backend

# Ver logs del frontend
docker-compose logs -f frontend

# Ver todos los logs
docker-compose logs -f
```

### Backups de Base de Datos

```bash
# Backup
docker exec crm_postgres pg_dump -U crm_user crm_analytics_db > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i crm_postgres psql -U crm_user crm_analytics_db < backup_20260504.sql
```

### Actualizaciones

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Seguridad en Producción

1. **Variables de Entorno**
   - Usar secretos fuertes
   - No commitear archivos .env
   - Usar servicios de gestión de secretos (AWS Secrets Manager, etc.)

2. **Base de Datos**
   - Usar contraseñas fuertes
   - Restringir acceso por IP
   - Habilitar SSL

3. **API**
   - Implementar rate limiting
   - Configurar CORS apropiadamente
   - Habilitar autenticación JWT

4. **Servidor**
   - Mantener sistema actualizado
   - Configurar firewall
   - Usar HTTPS siempre

## Troubleshooting

### Backend no inicia

```bash
# Verificar logs
docker-compose logs backend

# Verificar conexión a base de datos
docker-compose exec backend python -c "from app.core.database import engine; engine.connect()"
```

### Frontend no se conecta al backend

- Verificar que API_BASE_URL esté correctamente configurado
- Verificar que CORS esté configurado en el backend
- Revisar logs de ambos servicios

### Base de datos no inicia

```bash
# Verificar estado del contenedor
docker-compose ps postgres

# Verificar logs
docker-compose logs postgres

# Reiniciar servicio
docker-compose restart postgres
```

## Performance

### Optimización de PostgreSQL

```sql
-- Índices adicionales
CREATE INDEX idx_proyectos_estado ON proyectos(estado);
CREATE INDEX idx_tareas_estado ON tareas(estado);
CREATE INDEX idx_proyectos_cliente_id ON proyectos(cliente_id);
```

### Caché

Considerar agregar Redis para caché:

```yaml
# En docker-compose.yml
redis:
  image: redis:alpine
  ports:
    - "6379:6379"
```

## Escalabilidad

Para escalar horizontalmente:

1. Usar un load balancer (nginx, HAProxy, AWS ALB)
2. Múltiples instancias del backend
3. PostgreSQL con replicación
4. Caché distribuido (Redis Cluster)
