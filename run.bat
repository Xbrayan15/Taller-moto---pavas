@echo off
echo Iniciando API del Taller de Motos...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar si el entorno virtual existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    echo.
    echo Activando entorno virtual e instalando dependencias...
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    echo Activando entorno virtual...
    call venv\Scripts\activate
)

echo.
echo ========================================
echo API del Taller de Motos
echo ========================================
echo.
echo Documentación en: http://localhost:8000/docs
echo ReDoc en: http://localhost:8000/redoc
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python -m uvicorn app.main:app --reload
