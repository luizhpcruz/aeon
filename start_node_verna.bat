@echo off
title 🧠 AEON - V.E.R.N.A. Node
echo.
echo 🧠 INICIANDO NO V.E.R.N.A....
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
echo 🚀 Executando emergência simbólica...
python run_node_verna.py

echo.
echo ⏸️  Pressione qualquer tecla para fechar...
pause >nul
