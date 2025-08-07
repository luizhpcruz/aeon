@echo off
echo 🧬 AEON - Configuracao do Python
echo ================================

echo 🔍 Procurando instalacoes do Python...

REM Verifica se Python esta no PATH
where python >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python encontrado no PATH
    python --version
    goto :run_aeon
)

REM Procura Python 3.13
if exist "C:\Python313\python.exe" (
    echo ✅ Python 3.13 encontrado em C:\Python313\
    set PYTHON_CMD=C:\Python313\python.exe
    goto :run_aeon
)

REM Procura Python no AppData
for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Python encontrado em %%i
        set PYTHON_CMD=%%i\python.exe
        goto :run_aeon
    )
)

REM Procura Python no Program Files
for /d %%i in ("%PROGRAMFILES%\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Python encontrado em %%i
        set PYTHON_CMD=%%i\python.exe
        goto :run_aeon
    )
)

echo ❌ Python nao encontrado!
echo 📥 Instale Python de https://python.org
echo ⚠️  IMPORTANTE: Marque "Add Python to PATH" durante a instalacao
pause
exit /b 1

:run_aeon
echo.
echo 🚀 Executando AEON com Python encontrado...
echo.

if not defined PYTHON_CMD set PYTHON_CMD=python

echo 📊 Executando analise de entropia...
cd scripts
%PYTHON_CMD% 4.py
cd ..

echo.
echo ✅ Execucao concluida!
pause
