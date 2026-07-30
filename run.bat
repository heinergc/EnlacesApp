@echo off
REM ========================================
REM Script de inicio para la aplicación
REM Gestión de Enlaces
REM ========================================

echo.
echo ========================================
echo   APLICACION DE GESTION DE ENLACES
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde https://www.python.org
    echo.
    pause
    exit /b 1
)

echo [1/4] Python detectado correctamente
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [2/4] Creando entorno virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo Entorno virtual creado exitosamente
) else (
    echo [2/4] Entorno virtual ya existe
)
echo.

REM Activar el entorno virtual
echo [3/4] Activando entorno virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo.

REM Instalar/actualizar dependencias
echo [4/4] Instalando dependencias...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo.

echo ========================================
echo   MIGRANDO BASE DE DATOS...
echo ========================================
echo.
REM Ejecutar migración si existe la BD
if exist enlaces.db (
    python migrate_db.py
    echo.
)

echo ========================================
echo   INICIANDO SERVIDOR...
echo ========================================
echo.
echo La aplicacion estara disponible en:
echo http://localhost:5000
echo http://localhost:5000/dashboard  [NUEVO!]
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

REM Iniciar la aplicación
python app.py

REM Si el servidor se detiene, mostrar mensaje
echo.
echo ========================================
echo   SERVIDOR DETENIDO
echo ========================================
echo.
pause
