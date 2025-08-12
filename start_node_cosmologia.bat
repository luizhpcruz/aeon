@echo off
title 🌌 AEON - Cosmologia Node
echo.
echo 🌌 INICIANDO NO COSMOLOGIA...
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
echo 🚀 Executando simulação cosmológica...
python run_node_cosmologia.py

echo.
echo ⏸️  Pressione qualquer tecla para fechar...
pause >nul
