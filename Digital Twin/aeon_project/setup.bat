@echo off
echo 🚀 AEON Digital Twin - Setup Windows
echo =====================================

echo.
echo 🔍 Verificando Python...
py --version
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.10+ de: https://python.org
    pause
    exit /b 1
)

echo.
echo 🔄 Executando setup...
py setup.py

echo.
echo ✅ Setup concluído!
echo.
echo 🚀 Para executar o AEON:
echo    py -m streamlit run aeon_app.py
echo.
echo 🔍 Para verificar a rede:
echo    py status_checker.py
echo.
pause
