#!/bin/bash

# ========================================
# Script de inicio para la aplicación
# Gestión de Enlaces (Linux/Mac)
# ========================================

echo ""
echo "========================================"
echo "  APLICACIÓN DE GESTIÓN DE ENLACES"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "✅ [1/4] Python detectado correctamente"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "🔧 [2/4] Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: No se pudo crear el entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual creado exitosamente"
else
    echo "✅ [2/4] Entorno virtual ya existe"
fi
echo ""

# Activar el entorno virtual
echo "🔧 [3/4] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ ERROR: No se pudo activar el entorno virtual"
    exit 1
fi
echo ""

# Instalar/actualizar dependencias
echo "📦 [4/4] Instalando dependencias..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
echo ""

echo "========================================"
echo "  INICIANDO SERVIDOR..."
echo "========================================"
echo ""
echo "🌐 La aplicación estará disponible en:"
echo "   http://localhost:5000"
echo ""
echo "🛑 Presiona Ctrl+C para detener el servidor"
echo "========================================"
echo ""

# Iniciar la aplicación
python3 app.py

# Si el servidor se detiene, mostrar mensaje
echo ""
echo "========================================"
echo "  SERVIDOR DETENIDO"
echo "========================================"
echo ""
