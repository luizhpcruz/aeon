@echo off
cls
echo.
echo 🚀 AEON DIGITAL TWIN - DEMONSTRAÇÃO INTERATIVA MVP
echo ===================================================
echo 👨‍💻 Desenvolvido por: Luiz H. P. Cruz
echo 📅 Data: 03/08/2025
echo 🔬 Sistema: AEON Digital Twin Plataforma Completa
echo ===================================================
echo.

echo 📋 VERIFICANDO SISTEMA...
echo.

REM Verificar se o ambiente virtual existe
if exist ".venv\Scripts\python.exe" (
    echo ✅ Ambiente virtual Python - OK
    set PYTHON_CMD=.venv\Scripts\python.exe
) else (
    echo ❌ Ambiente virtual não encontrado. Usando Python sistema.
    set PYTHON_CMD=python
)

REM Verificar módulos principais
echo.
echo 🔍 Verificando módulos AEON...

if exist "scripts\4.py" (
    echo ✅ Análise de Entropia (4.py) - OK
) else (
    echo ❌ scripts\4.py não encontrado
)

if exist "scripts\VERNA.py" (
    echo ✅ V.E.R.N.A. AI System - OK
) else (
    echo ❌ scripts\VERNA.py não encontrado
)

if exist "scripts\NMD.py" (
    echo ✅ Cosmologia NMD - OK
) else (
    echo ❌ scripts\NMD.py não encontrado
)

if exist "backend\main.py" (
    echo ✅ Backend FastAPI - OK
) else (
    echo ❌ backend\main.py não encontrado
)

if exist "frontend\index.html" (
    echo ✅ Frontend HTML/JS - OK
) else (
    echo ❌ frontend\index.html não encontrado
)

echo.
echo 📦 Instalando dependências necessárias...
%PYTHON_CMD% -m pip install --quiet fastapi uvicorn numpy matplotlib pandas seaborn scipy scikit-learn

echo.
echo 🚀 OPÇÕES DE DEMONSTRAÇÃO:
echo.
echo [1] Executar análise de entropia completa (4.py)
echo [2] Iniciar servidor MVP interativo (FastAPI + Frontend)
echo [3] Teste rápido de funcionalidades
echo [4] Demonstração completa (Recomendado)
echo [5] Sair
echo.

set /p choice="Escolha uma opção (1-5): "

if "%choice%"=="1" goto :entropia
if "%choice%"=="2" goto :servidor
if "%choice%"=="3" goto :teste
if "%choice%"=="4" goto :completa
if "%choice%"=="5" goto :fim

:entropia
echo.
echo 🧬 EXECUTANDO ANÁLISE DE ENTROPIA AEON...
echo ========================================
%PYTHON_CMD% scripts\4.py
pause
goto :menu

:servidor
echo.
echo 🌐 INICIANDO SERVIDOR MVP INTERATIVO...
echo =====================================
echo Frontend: http://localhost:8000/
echo API Docs: http://localhost:8000/docs
echo.
cd backend
%PYTHON_CMD% -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
goto :fim

:teste
echo.
echo ⚡ TESTE RÁPIDO DE FUNCIONALIDADES...
echo ===================================
%PYTHON_CMD% teste_simples.py
pause
goto :menu

:completa
echo.
echo 🎯 DEMONSTRAÇÃO COMPLETA AEON MVP
echo =================================
echo.
echo Executando em sequência:
echo 1. Teste de funcionalidades básicas
echo 2. Análise de entropia (primeiros 20 ciclos)
echo 3. Inicialização do servidor MVP
echo.
pause

echo 📊 1/3 - Teste básico...
%PYTHON_CMD% teste_simples.py

echo.
echo 🧬 2/3 - Análise entropia (versão rápida)...
%PYTHON_CMD% demo_aeon_interactive.py

echo.
echo 🌐 3/3 - Servidor MVP (pressione Ctrl+C para parar)...
echo Frontend: http://localhost:8000/
echo API Docs: http://localhost:8000/docs
echo.
start "" "http://localhost:8000/"
cd backend
%PYTHON_CMD% -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
goto :fim

:menu
echo.
goto :inicio

:fim
echo.
echo 🎉 Demonstração AEON finalizada!
echo Obrigado por usar o AEON Digital Twin MVP.
echo.
pause
