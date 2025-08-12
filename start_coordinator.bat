@echo off
title 🎯 AEON - Coordinator Node
echo.
echo 🎯 INICIANDO COORDENADOR...
echo ================================================
echo.

REM Ativar venv se existir
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment ativado
) else (
    echo ⚠️  Executando sem venv
)

echo.
echo 🔍 Aguardando resultados dos nós...
echo ⏰ Timeout: 30 segundos
echo.
python run_coordinator.py

echo.
echo ⏸️  Pressione qualquer tecla para fechar...
pause >nul
