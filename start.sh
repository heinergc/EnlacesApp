#!/bin/bash
# Script de inicio para producción en Render.com

# Crear directorio para la base de datos si no existe
mkdir -p /opt/render/project/data

# Iniciar la aplicación con Gunicorn
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 app:app
