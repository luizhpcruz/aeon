@echo off
REM 🚀 AEONCOSMA Engine - Setup Script for Windows
REM Configuração automática do ambiente AEONCOSMA
REM Copyright 2025 - Luiz H. P. Cruz

echo.
echo ====================================================================
echo 🌟 AEONCOSMA Engine - Setup Script
echo Plataforma Modular: IA + Blockchain + P2P + Quantum + Cosmos
echo Autor: Luiz H. P. Cruz
echo ====================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.10+ primeiro.
    echo 💡 Download: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Verificar versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 📋 Versão do Python: %PYTHON_VERSION%

REM Criar ambiente virtual
echo.
echo 📦 Criando ambiente virtual...
if exist "aeoncosma_env" (
    echo ⚠️  Ambiente virtual já existe. Removendo...
    rmdir /s /q aeoncosma_env
)

python -m venv aeoncosma_env
if errorlevel 1 (
    echo ❌ Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo ✅ Ambiente virtual criado

REM Ativar ambiente virtual
echo.
echo 🔧 Ativando ambiente virtual...
call aeoncosma_env\Scripts\activate.bat

REM Atualizar pip
echo.
echo 📥 Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo.
echo 📚 Instalando dependências do AEONCOSMA...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Erro na instalação das dependências
    echo 💡 Verifique sua conexão com a internet
    pause
    exit /b 1
)

echo ✅ Dependências instaladas com sucesso

REM Criar diretórios necessários
echo.
echo 📁 Criando estrutura de diretórios...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "config" mkdir config
if not exist "temp" mkdir temp

echo ✅ Estrutura criada

REM Verificar instalação dos módulos principais
echo.
echo 🔍 Verificando instalação dos módulos...

python -c "import fastapi; print('✅ FastAPI instalado')" 2>nul || echo "❌ Erro: FastAPI"
python -c "import streamlit; print('✅ Streamlit instalado')" 2>nul || echo "❌ Erro: Streamlit"
python -c "import cryptography; print('✅ Cryptography instalado')" 2>nul || echo "❌ Erro: Cryptography"
python -c "import numpy; print('✅ NumPy instalado')" 2>nul || echo "❌ Erro: NumPy"
python -c "import scipy; print('✅ SciPy instalado')" 2>nul || echo "❌ Erro: SciPy"

REM Criar arquivo de configuração inicial
echo.
echo ⚙️  Criando configuração inicial...
echo {> config\aeoncosma_config.json
echo   "system": {>> config\aeoncosma_config.json
echo     "version": "1.0.0",>> config\aeoncosma_config.json
echo     "author": "Luiz H. P. Cruz",>> config\aeoncosma_config.json
echo     "environment": "development",>> config\aeoncosma_config.json
echo     "debug": true>> config\aeoncosma_config.json
echo   },>> config\aeoncosma_config.json
echo   "api": {>> config\aeoncosma_config.json
echo     "host": "0.0.0.0",>> config\aeoncosma_config.json
echo     "port": 8000>> config\aeoncosma_config.json
echo   },>> config\aeoncosma_config.json
echo   "ui": {>> config\aeoncosma_config.json
echo     "host": "localhost",>> config\aeoncosma_config.json
echo     "port": 8501>> config\aeoncosma_config.json
echo   }>> config\aeoncosma_config.json
echo }>> config\aeoncosma_config.json

echo ✅ Configuração criada

REM Criar scripts de execução
echo.
echo 📝 Criando scripts de execução...

REM Script para API
echo @echo off> start_api.bat
echo echo 🚀 Iniciando AEONCOSMA API...>> start_api.bat
echo call aeoncosma_env\Scripts\activate.bat>> start_api.bat
echo python aeoncosma_api.py>> start_api.bat
echo pause>> start_api.bat

REM Script para UI
echo @echo off> start_ui.bat
echo echo 🌟 Iniciando AEONCOSMA Interface...>> start_ui.bat
echo call aeoncosma_env\Scripts\activate.bat>> start_ui.bat
echo streamlit run ui\streamlit_interface.py>> start_ui.bat
echo pause>> start_ui.bat

REM Script completo
echo @echo off> start_aeoncosma.bat
echo echo 🌟 Iniciando AEONCOSMA Engine Completo...>> start_aeoncosma.bat
echo call aeoncosma_env\Scripts\activate.bat>> start_aeoncosma.bat
echo echo.>> start_aeoncosma.bat
echo echo 🚀 Iniciando API em segundo plano...>> start_aeoncosma.bat
echo start /B python aeoncosma_api.py>> start_aeoncosma.bat
echo timeout /t 5 /nobreak ^>nul>> start_aeoncosma.bat
echo echo.>> start_aeoncosma.bat
echo echo 🌟 Iniciando Interface Web...>> start_aeoncosma.bat
echo streamlit run ui\streamlit_interface.py>> start_aeoncosma.bat

echo ✅ Scripts criados

REM Mostrar informações finais
echo.
echo ====================================================================
echo 🎉 SETUP CONCLUÍDO COM SUCESSO!
echo ====================================================================
echo.
echo 📋 Próximos passos:
echo.
echo 1️⃣  Para iniciar apenas a API:
echo    👉 start_api.bat
echo    🌐 Acesse: http://localhost:8000/docs
echo.
echo 2️⃣  Para iniciar apenas a Interface:
echo    👉 start_ui.bat
echo    🌐 Acesse: http://localhost:8501
echo.
echo 3️⃣  Para iniciar tudo junto:
echo    👉 start_aeoncosma.bat
echo.
echo 📚 Documentação completa:
echo    👉 README.md
echo.
echo 🛠️  Configurações em:
echo    👉 config\aeoncosma_config.json
echo.
echo 📊 Logs em:
echo    👉 logs\
echo.
echo ====================================================================
echo 🌟 AEONCOSMA Engine - Criado por Luiz H. P. Cruz
echo 💡 IA + Blockchain + P2P + Quantum + Cosmos
echo ====================================================================
echo.

pause
