@echo off
REM Script de Instalação do Módulo Bayesiano AEON
REM =============================================

echo 🚀 AEON - Instalação do Módulo Bayesiano
echo ===============================================
echo.

echo 📦 Instalando dependências para análise Bayesiana...
echo.

REM Verificar se pip está disponível
py -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip não encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

echo ✅ pip encontrado, prosseguindo com instalação...
echo.

REM Instalar dependências principais
echo 🔧 Instalando PyMC e ArviZ...
py -m pip install pymc arviz

echo 🔧 Instalando dependências numéricas...
py -m pip install numpy pandas scipy

echo 🔧 Instalando visualização...
py -m pip install matplotlib seaborn

echo 🔧 Instalando utilitários...
py -m pip install ipython jupyter

echo.
echo ✅ Instalação concluída!
echo.

REM Executar teste de validação
echo 🧪 Executando teste de validação...
echo.
py test_bayesian.py

echo.
echo 🎯 Instalação do Módulo Bayesiano AEON finalizada!
echo.
echo 📋 Próximos passos:
echo   1. Execute: py src\bayesian\mcmc_real.py
echo   2. Verifique os arquivos gerados (*.png, *.nc)
echo   3. Integre com os dados reais do sistema AEON
echo.
pause
