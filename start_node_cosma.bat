@echo off
title 🤖 AEON - Cosma Node
echo.
echo 🤖 INICIANDO NO AEON COSMA...
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
echo 🚀 Executando motor cosmológico inteligente...
python run_node_cosma.py

echo.
echo ⏸️  Pressione qualquer tecla para fechar...
pause >nul
