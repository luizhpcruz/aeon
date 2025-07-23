@echo off
title AEON - Setup do Ambiente
color 0B

echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║            🚀 AEON - SETUP DO AMBIENTE 🚀               ║
echo     ║              Configuração Automática                    ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo 📥 Por favor, instale Python 3.8+ de https://python.org
    echo ⚙️  Certifique-se de marcar "Add Python to PATH" durante a instalação
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version

echo.
echo 📦 Criando ambiente virtual Python...
if exist "venv\" (
    echo ⚠️  Ambiente virtual já existe. Removendo...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo ✅ Ambiente virtual criado com sucesso!

echo.
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate

echo.
echo 📚 Atualizando pip e instalando dependências...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Aviso: Não foi possível atualizar pip
)

pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    echo 🔍 Verifique se o arquivo requirements.txt existe
    pause
    exit /b 1
)

echo.
echo ✅ Verificando instalação das bibliotecas principais...
python -c "import numpy; print('✅ NumPy:', numpy.__version__)" 2>nul || echo "❌ NumPy não instalado"
python -c "import matplotlib; print('✅ Matplotlib:', matplotlib.__version__)" 2>nul || echo "❌ Matplotlib não instalado"
python -c "import seaborn; print('✅ Seaborn:', seaborn.__version__)" 2>nul || echo "❌ Seaborn não instalado"
python -c "import pandas; print('✅ Pandas:', pandas.__version__)" 2>nul || echo "❌ Pandas não instalado"

echo.
echo 🔧 Configurando Git (se necessário)...
git --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Git não encontrado. Instale Git para versionamento.
) else (
    git config --global init.defaultBranch main 2>nul
    echo ✅ Git configurado!
)

echo.
echo 📁 Verificando estrutura de pastas...
if not exist "scripts\" mkdir scripts
if not exist "data\" mkdir data
if not exist "visualizations\" mkdir visualizations
if not exist "docs\" mkdir docs
echo ✅ Estrutura de pastas verificada!

echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                🎉 SETUP CONCLUÍDO! 🎉                   ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.
echo 📋 PRÓXIMOS PASSOS:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  1. Execute 'run.bat' para usar o sistema
echo  2. Escolha a opção 1 (Análise de Entropia) para começar
echo  3. Consulte README.md para documentação completa
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📖 Documentação disponível em docs/
echo 🌐 Frontend React disponível em frontend/
echo 🔬 Scripts Python em scripts/
echo.
pause
