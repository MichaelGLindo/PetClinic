@echo off

echo Verificando Python...
python --version

echo.
echo Creando entorno virtual...
python -m venv .venv

echo.
echo Activando entorno virtual...
call .venv\Scripts\activate

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando FastAPI...
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

pause