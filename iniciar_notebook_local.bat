@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\jupyter-notebook.exe" (
  echo No se encontro el entorno local.
  echo Ejecuta primero instalar_entorno_local.bat
  pause
  exit /b 1
)
".venv\Scripts\jupyter-notebook.exe" "YOLOv5_alumnos.ipynb"
