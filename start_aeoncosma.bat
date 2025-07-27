@echo off
echo 🌌 INICIANDO AEONCOSMA PREDICTOR...
echo ===================================
cd /d "%~dp0"
echo Tentando iniciar servidor...
py test_server.py
if errorlevel 1 (
    echo Tentando com python...
    python test_server.py
)
pause
