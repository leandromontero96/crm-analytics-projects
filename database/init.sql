-- Script de inicialización de la base de datos
-- Este script se ejecutará automáticamente al crear la base de datos

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Crear índices adicionales para mejor performance
-- Los índices principales se crean automáticamente por SQLAlchemy

-- Comentarios en tablas (se crearán después de que SQLAlchemy cree las tablas)
COMMENT ON TABLE clientes IS 'Tabla de clientes del CRM';
COMMENT ON TABLE proyectos IS 'Tabla de proyectos de análisis de datos';
COMMENT ON TABLE tareas IS 'Tabla de tareas asociadas a proyectos';
COMMENT ON TABLE entregables IS 'Tabla de entregables de proyectos';
COMMENT ON TABLE usuarios IS 'Tabla de usuarios del sistema';
