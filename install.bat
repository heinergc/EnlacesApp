@echo off
REM ========================================
REM Script de instalación mejorado
REM ========================================

echo.
echo ========================================
echo   INSTALACION - GESTION DE ENLACES
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python instalado

REM Verificar pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] pip no disponible, intentando reparar...
    python -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo [!] No se pudo instalar pip automaticamente
        echo.
        echo SOLUCION: Reinstala Python con estas opciones:
        echo   - Marca "Add Python to PATH"
        echo   - Marca "pip"
        echo   - Usa "Install for all users"
        echo.
        pause
        exit /b 1
    )
)

echo [OK] pip instalado

REM Actualizar pip
echo.
echo Actualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar dependencias directamente (sin venv)
echo.
echo Instalando dependencias...
python -m pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo Para ejecutar la aplicacion usa:
echo   start.bat
echo.
pause
