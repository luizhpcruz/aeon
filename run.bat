@echo off
title AEON - Sistema de Simulação Complexa
color 0A

echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║               🧬 AEON - Sistema COMPLEXO 🧬              ║
echo     ║                    Sistema de Simulação                  ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Verificar se está no diretório correto
if not exist "scripts\" (
    echo ❌ Erro: Execute este script na pasta raiz do projeto AEON
    pause
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist "venv\" (
    echo 🔧 Ativando ambiente virtual...
    call venv\Scripts\activate
    echo ✅ Ambiente virtual ativado
) else (
    echo ⚠️  Ambiente virtual não encontrado. Execute setup.bat primeiro.
)

echo.
echo 📋 OPÇÕES DISPONÍVEIS:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  1. 🔬 Executar Análise de Entropia (Recomendado)
echo  2. 🌌 Executar Modelo Cosmológico
echo  3. 🤖 Executar Motor AEON Cosma
echo  4. 🧠 Executar Sistema V.E.R.N.A.
echo  5. 📊 Executar TODAS as simulações
echo  6. 🚀 Instalar/Atualizar dependências
echo  7. 📁 Abrir pasta de resultados
echo  8. 🔄 Status do projeto
echo  0. ❌ Sair
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

set /p choice="🎯 Digite sua escolha (0-8): "

if "%choice%"=="1" (
    echo.
    echo 🔬 Executando análise de entropia...
    cd scripts
    python 4.py
    cd ..
) else if "%choice%"=="2" (
    echo.
    echo 🌌 Executando modelo cosmológico...
    cd scripts
    python NMD.py
    cd ..
) else if "%choice%"=="3" (
    echo.
    echo 🤖 Executando motor AEON Cosma...
    cd bagunça\AEONCOSMA_ENGINE_v1
    python aeon_interface.py
    cd ..\..
) else if "%choice%"=="4" (
    echo.
    echo 🧠 Executando sistema V.E.R.N.A...
    python teoria\verna.py
) else if "%choice%"=="5" (
    echo.
    echo 📊 Executando TODAS as simulações...
    echo ⏳ Isso pode levar alguns minutos...
    cd scripts
    for %%f in (1.py 2.py 3.py 4.py 5.py) do (
        echo 🔄 Executando %%f...
        python %%f
    )
    cd ..
) else if "%choice%"=="6" (
    echo.
    echo 🚀 Instalando/Atualizando dependências...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else if "%choice%"=="7" (
    echo.
    echo 📁 Abrindo pasta de resultados...
    if exist "data\" explorer data
    if exist "visualizations\" explorer visualizations
) else if "%choice%"=="8" (
    echo.
    echo 🔄 STATUS DO PROJETO AEON:
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if exist "venv\" (echo ✅ Ambiente virtual: OK) else (echo ❌ Ambiente virtual: NÃO ENCONTRADO)
    if exist "scripts\4.py" (echo ✅ Scripts principais: OK) else (echo ❌ Scripts: PROBLEMA)
    if exist "data\" (echo ✅ Pasta de dados: OK) else (echo ❌ Pasta de dados: PROBLEMA)
    if exist "visualizations\" (echo ✅ Pasta de visualizações: OK) else (echo ❌ Visualizações: PROBLEMA)
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
) else if "%choice%"=="0" (
    echo.
    echo 👋 Até logo! Sistema AEON finalizado.
    exit /b 0
) else (
    echo.
    echo ❌ Opção inválida. Tente novamente.
)

echo.
echo ✨ Operação concluída!
echo 📖 Consulte o README.md para mais informações
echo.
pause
