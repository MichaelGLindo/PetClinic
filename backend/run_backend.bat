@echo off
SETLOCAL EnableDelayedExpansion
title PetClinic Backend Runner

echo ===================================================
echo   PetClinic FastAPI Backend Setup and Runner
echo ===================================================
echo.

:: Check for python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH.
    echo.
    echo Por favor, instale Python (version 3.10 o superior) desde:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Asegurese de marcar la casilla "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist .venv (
    echo [INFO] Creando entorno virtual .venv...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo [INFO] Activando entorno virtual...
call .venv\Scripts\activate

:: Install/Upgrade requirements
echo [INFO] Instalando dependencias desde requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo [ERROR] Fallo la instalacion de dependencias.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Backend configurado correctamente.
echo [INFO] Iniciando el servidor FastAPI en http://localhost:8080...
echo [INFO] Presione Ctrl+C para detener el servidor.
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
