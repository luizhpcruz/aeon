@echo off
title 🔬 AEON - Entropy Node
echo.
echo 🔬 INICIANDO NO ENTROPY...
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
echo 🚀 Executando simulação de entropia...
python run_node_entropy.py

echo.
echo ⏸️  Pressione qualquer tecla para fechar...
pause >nul
