#!/bin/bash

echo "Iniciando API del Taller de Motos..."
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo ""
    echo "Activando entorno virtual e instalando dependencias..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

echo ""
echo "========================================"
echo "API del Taller de Motos"
echo "========================================"
echo ""
echo "Documentación en: http://localhost:8000/docs"
echo "ReDoc en: http://localhost:8000/redoc"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python -m uvicorn app.main:app --reload
