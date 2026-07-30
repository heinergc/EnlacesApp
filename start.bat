@echo off
REM ========================================
REM Script de inicio simplificado (sin venv)
REM ========================================

echo.
echo ========================================
echo   GESTION DE ENLACES
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    echo Ejecuta primero: install.bat
    pause
    exit /b 1
)

REM Migrar BD si existe
if exist enlaces.db (
    echo Migrando base de datos...
    python migrate_db.py
    echo.
)

REM Iniciar aplicación
echo ========================================
echo   INICIANDO SERVIDOR...
echo ========================================
echo.
echo Aplicacion disponible en:
echo   http://localhost:5000
echo   http://localhost:5000/dashboard  [DASHBOARD NUEVO]
echo.
echo Presiona Ctrl+C para detener
echo ========================================
echo.

python app.py

REM Si se detiene
echo.
echo Servidor detenido
pause
