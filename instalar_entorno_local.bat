@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" py -3.12 -m venv .venv
if not exist "vendor\yolov5\train.py" (
  git clone https://github.com/ultralytics/yolov5.git vendor\yolov5
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r "vendor\yolov5\requirements.txt" notebook ipykernel
if errorlevel 1 (
  echo Error instalando el entorno.
  pause
  exit /b 1
)
echo Entorno instalado correctamente.
pause
