@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" "scripts\local_smoke_test.py"
if errorlevel 1 (
  echo La prueba local fallo.
  pause
  exit /b 1
)
echo La prueba local termino correctamente.
pause
