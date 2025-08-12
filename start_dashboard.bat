@echo off
set AEON_QUIET=1
echo 🌟 INICIANDO AEON DASHBOARD...
echo.
echo 📊 Interface Web Unificada dos Sistemas AEON
echo 🔗 URL: http://localhost:8501
echo.
echo ⚡ Aguarde o navegador abrir...
echo.

cd /d "%~dp0"
call .\venv\Scripts\activate.bat 2>nul || echo Ambiente virtual não encontrado, usando Python global...
streamlit run aeon_dashboard.py --server.port 8501 --server.headless false

pause
